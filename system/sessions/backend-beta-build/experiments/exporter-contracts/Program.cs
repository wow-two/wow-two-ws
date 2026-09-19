using System.Globalization;
using System.Text;
using ClosedXML.Excel;
using WoW.Two.Sdk.Backend.Beta.Media.Csv.Exporters;
using WoW.Two.Sdk.Backend.Beta.Media.Excel.Exporters;
using WoW.Two.Sdk.Backend.Beta.Media.Tabular.Exporters;

CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("fr-FR");
var row = new Row { Zebra = "é,quoted", Amount = 12.5m, When = new DateTime(2026, 9, 15), Alpha = "tail" };
Console.WriteLine($"Runtime={Environment.Version}; Culture={CultureInfo.CurrentCulture.Name}; ClosedXML={typeof(XLWorkbook).Assembly.GetName().Version}; CsvHelper={typeof(CsvHelper.CsvWriter).Assembly.GetName().Version}");
foreach (ITabularExporter exporter in new ITabularExporter[] { new CsvTabularExporter(), new ExcelTabularExporter() })
{
    Console.WriteLine($"\nEXPORTER={exporter.GetType().Name}");
    await Run("normal", exporter, new[] { row });
    await Run("empty", exporter, Array.Empty<Row>());
    await Run("fields", exporter, new[] { new FieldRow() });
    await Run("attributes", exporter, new[] { new AttributeRow() });
    await Run("class-attributes", exporter, new[] { new ConfigurationRow() });
    await Run("scalar", exporter, new[] { 12, 34 });
    await Run("empty-scalar", exporter, Array.Empty<int>());
    await Run("nonseekable", exporter, new[] { row }, nonSeekable: true);
    await Run("nonseekable-prefix", exporter, new[] { row }, nonSeekable: true, prefix: 8);
    await Run("position-prefix", exporter, new[] { row }, prefix: 8);
    await Run("writeonly-seekable-prefix", exporter, new[] { row }, prefix: 8, canRead: false);
    await Run("overwrite-existing", exporter, new[] { row }, tail: 20000);
    await Run("enumeration-fails", exporter, Fails(row));
    await Run("destination-fails", exporter, new[] { row }, failAfter: 12);
    using var already = new CancellationTokenSource();
    already.Cancel();
    await Run("pre-canceled", exporter, new[] { row }, token: already.Token);
    using var during = new CancellationTokenSource();
    await Run("mid-enumeration-canceled", exporter, Cancels(row, during), token: during.Token);
    var enumerationCount = 0;
    IEnumerable<Row> CountedRows() { enumerationCount++; yield return row; }
    await Run("enumeration-count", exporter, CountedRows());
    Console.WriteLine($"  enumerationCount={enumerationCount}");
}

var assertions = 0;
var csvExporter = new CsvTabularExporter();
using (var canceled = new CancellationTokenSource())
using (var destination = new MemoryStream())
{
    canceled.Cancel();
    var exception = await Capture(() => csvExporter.WriteAsync(new[] { row }, destination, canceled.Token));
    Check(exception is OperationCanceledException, "CSV pre-cancel exposes OperationCanceledException");
    Check(((OperationCanceledException)exception!).CancellationToken == canceled.Token, "CSV pre-cancel preserves caller token");
    Check(destination.Length == 0, "CSV pre-cancel writes no bytes");
}
using (var canceled = new CancellationTokenSource())
using (var destination = new MemoryStream())
{
    var exception = await Capture(() => csvExporter.WriteAsync(Cancels(row, canceled), destination, canceled.Token));
    Check(exception is OperationCanceledException, "CSV mid-cancel exposes OperationCanceledException");
    Check(((OperationCanceledException)exception!).CancellationToken == canceled.Token, "CSV mid-cancel preserves caller token");
    Check(destination.Length > 0, "CSV mid-cancel can leave partial bytes");
}
using (var canceled = new CancellationTokenSource())
using (var destination = new MemoryStream())
{
    var exception = await Capture(() => csvExporter.WriteAsync(CancelsAndFails(row, canceled), destination, canceled.Token));
    Check(exception is CsvHelper.WriterException { InnerException: InvalidOperationException }, "CSV non-cancellation failure remains WriterException even when token canceled");
}
Console.WriteLine($"ASSERTIONS PASSED={assertions}");

void Check(bool condition, string description)
{
    if (!condition) throw new InvalidOperationException($"ASSERTION FAILED: {description}");
    assertions++;
    Console.WriteLine($"PASS: {description}");
}

static async Task<Exception?> Capture(Func<Task> action)
{
    try { await action(); return null; }
    catch (Exception exception) { return exception; }
}

static IEnumerable<Row> CancelsAndFails(Row row, CancellationTokenSource source)
{
    yield return row;
    source.Cancel();
    throw new InvalidOperationException("diagnostic non-cancellation failure");
}

static IEnumerable<Row> Fails(Row row)
{
    yield return row;
    throw new InvalidOperationException("diagnostic enumeration failure");
}

static IEnumerable<Row> Cancels(Row row, CancellationTokenSource source)
{
    yield return row;
    source.Cancel();
    yield return row;
    yield return row;
}

static async Task Run<T>(string label, ITabularExporter exporter, IEnumerable<T> rows, bool nonSeekable = false, int prefix = 0, int tail = 0, CancellationToken token = default, int failAfter = int.MaxValue, bool canRead = true)
{
    using var data = new MemoryStream();
    if (prefix != 0) data.Write(Encoding.UTF8.GetBytes(new string('P', prefix)));
    if (tail != 0) { data.Write(new byte[tail]); data.Position = 0; }
    using var target = new ProbeStream(data, nonSeekable, failAfter, canRead);
    string outcome;
    try { await exporter.WriteAsync(rows, target, token); outcome = "success"; }
    catch (Exception ex) { outcome = $"{ex.GetType().Name}: {ex.Message.Split('\n')[0]}; inner={ex.InnerException?.GetType().Name}: {ex.InnerException?.Message.Split('\n')[0]}"; }
    var bytes = data.ToArray();
    Console.WriteLine($"{label}: {outcome}; length={data.Length}; position={data.Position}; open={!target.Disposed}; seekCalls={target.SeekCalls}; setLengthCalls={target.SetLengthCalls}; tokenCanceled={token.IsCancellationRequested}");
    if (exporter is CsvTabularExporter)
        Console.WriteLine($"  utf8Bom={bytes.AsSpan().StartsWith(new byte[] { 239, 187, 191 })}; output={System.Text.Json.JsonSerializer.Serialize(Encoding.UTF8.GetString(bytes.Length > 100 ? bytes[..100] : bytes))}");
    else if (outcome == "success")
    {
        try
        {
            using var workbook = new XLWorkbook(new MemoryStream(bytes));
            var sheet = workbook.Worksheet(1);
            var used = sheet.RangeUsed();
            Console.WriteLine($"  workbookReadable=true; sheets={workbook.Worksheets.Count}; name={sheet.Name}; tables={sheet.Tables.Count()}; range={used?.RangeAddress}");
            foreach (var r in sheet.RowsUsed().Take(4))
                Console.WriteLine($"  cells={string.Join(" | ", r.CellsUsed().Select(c => $"{c.GetString()}<{c.DataType}>[format:{c.Style.NumberFormat.NumberFormatId}/{c.Style.NumberFormat.Format}]"))}");
        }
        catch (Exception ex) { Console.WriteLine($"  workbookReadable=false; {ex.GetType().Name}: {ex.Message}"); }
    }
}

public sealed record Row
{
    public string Zebra { get; init; } = "";
    public decimal Amount { get; init; }
    public DateTime When { get; init; }
    public string Alpha { get; init; } = "";
}

public sealed class FieldRow
{
    public string Field = "public-field";
    public string Property { get; set; } = "public-property";
    public static string StaticProperty => "static-property";
}

[CsvHelper.Configuration.Attributes.Delimiter(";")]
[CsvHelper.Configuration.Attributes.CultureInfo("fr-FR")]
public sealed class ConfigurationRow
{
    public string Name { get; set; } = "row";
    public decimal Amount { get; set; } = 12.5m;
}

public sealed class AttributeRow
{
    [ClosedXML.Attributes.XLColumn(Header = "xlsx-last", Order = 2)]
    [CsvHelper.Configuration.Attributes.Name("csv-last")]
    [CsvHelper.Configuration.Attributes.Index(2)]
    public string A { get; set; } = "a";
    [ClosedXML.Attributes.XLColumn(Header = "xlsx-first", Order = 1)]
    [CsvHelper.Configuration.Attributes.Name("csv-first")]
    [CsvHelper.Configuration.Attributes.Index(1)]
    public string Z { get; set; } = "z";
    [ClosedXML.Attributes.XLColumn(Ignore = true)]
    [CsvHelper.Configuration.Attributes.Ignore]
    public string Hidden { get; set; } = "hidden";
}

public sealed class ProbeStream(MemoryStream inner, bool nonSeekable, int failAfter, bool canRead) : Stream
{
    public bool Disposed { get; private set; }
    public int SeekCalls { get; private set; }
    public int SetLengthCalls { get; private set; }
    public override bool CanRead => !nonSeekable && canRead;
    public override bool CanSeek => !nonSeekable;
    public override bool CanWrite => !Disposed;
    public override long Length => nonSeekable ? throw new NotSupportedException() : inner.Length;
    public override long Position { get => nonSeekable ? throw new NotSupportedException() : inner.Position; set { if (nonSeekable) throw new NotSupportedException(); SeekCalls++; inner.Position = value; } }
    public override void Flush() => inner.Flush();
    public override Task FlushAsync(CancellationToken token) => inner.FlushAsync(token);
    public override int Read(byte[] buffer, int offset, int count) => !CanRead ? throw new NotSupportedException() : inner.Read(buffer, offset, count);
    public override long Seek(long offset, SeekOrigin origin) { if (nonSeekable) throw new NotSupportedException(); SeekCalls++; return inner.Seek(offset, origin); }
    public override void SetLength(long value) { if (nonSeekable) throw new NotSupportedException(); SetLengthCalls++; inner.SetLength(value); }
    public override void Write(byte[] buffer, int offset, int count) => Write(buffer.AsSpan(offset, count));
    public override void Write(ReadOnlySpan<byte> buffer)
    {
        var available = Math.Max(0, failAfter - (int)inner.Position);
        inner.Write(buffer[..Math.Min(buffer.Length, available)]);
        if (buffer.Length > available) throw new IOException("diagnostic destination failure");
    }
    public override Task WriteAsync(byte[] buffer, int offset, int count, CancellationToken token)
    {
        token.ThrowIfCancellationRequested();
        Write(buffer, offset, count);
        return Task.CompletedTask;
    }
    protected override void Dispose(bool disposing) { Disposed = true; base.Dispose(disposing); }
}
