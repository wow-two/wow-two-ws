using System.Reflection;
using System.Runtime.InteropServices;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;

Console.WriteLine($"ENV runtime={RuntimeInformation.FrameworkDescription} arch={RuntimeInformation.ProcessArchitecture} EF={typeof(DbContext).Assembly.GetCustomAttribute<AssemblyInformationalVersionAttribute>()!.InformationalVersion} SQLiteProvider={typeof(SqliteConnection).Assembly.GetCustomAttribute<AssemblyInformationalVersionAttribute>()!.InformationalVersion}");
var passed = 0;
var failed = 0;
void Check(string label, bool condition, string observation)
{
    Console.WriteLine($"{(condition ? "PASS" : "FAIL")} {label}: {observation}");
    if (condition) passed++; else failed++;
}
void Conflict(string label, Action action)
{
    try { action(); Check(label, false, "No exception"); }
    catch (InvalidOperationException e)
    {
        Check(label, e.Message.Contains("cannot be tracked") && e.Message.Contains("already being tracked"), e.Message);
    }
}
using var connection = new SqliteConnection("Data Source=:memory:");
connection.Open();
using (var cmd = connection.CreateCommand())
{
    cmd.CommandText = "select sqlite_version()";
    Console.WriteLine($"ENV SQLite={cmd.ExecuteScalar()}");
}
var options = new DbContextOptionsBuilder<ExperimentContext>().UseSqlite(connection).Options;
ExperimentContext Context() => new(options);
using (var db = Context()) db.Database.EnsureCreated();

// Baseline: mutable, sealed record and mutable, sealed class use identical tracking operations.
int recordId, classId;
using (var db = Context())
{
    var record = new RecordEntity { Name = "before" };
    var entity = new ClassEntity { Name = "before" };
    db.AddRange(record, entity);
    db.SaveChanges();
    recordId = record.Id; classId = entity.Id;
    Check("normal.insert", recordId > 0 && classId > 0, $"record.Id={recordId}, class.Id={classId}");
}
using (var db = Context())
{
    var record = db.Records.Single(x => x.Id == recordId);
    var entity = db.Classes.Single(x => x.Id == classId);
    record.Name = "mutated"; entity.Name = "mutated";
    db.ChangeTracker.DetectChanges();
    Check("normal.detect-change", db.Entry(record).State == EntityState.Modified && db.Entry(entity).State == EntityState.Modified,
        $"record={db.Entry(record).State}, class={db.Entry(entity).State}");
    db.SaveChanges();
    record.Name = "mutated-again"; entity.Name = "mutated-again";
    db.SaveChanges();
}
using (var db = Context())
    Check("normal.persist-two-mutations", db.Records.Find(recordId)!.Name == "mutated-again" && db.Classes.Find(classId)!.Name == "mutated-again", "fresh context persisted both second changes");

foreach (var useUpdate in new[] { false, true })
{
    using (var db = Context())
    {
        var original = db.Records.Find(recordId)!;
        var copy = original with { Name = "record-copy" };
        Conflict($"same-key.record.{(useUpdate ? "Update" : "Attach")}", () => { if (useUpdate) db.Update(copy); else db.Attach(copy); });
    }
    using (var db = Context())
    {
        var original = db.Classes.Find(classId)!;
        var copy = new ClassEntity { Id = original.Id, Name = "class-copy", GroupId = original.GroupId };
        Conflict($"same-key.class.{(useUpdate ? "Update" : "Attach")}", () => { if (useUpdate) db.Update(copy); else db.Attach(copy); });
    }
}
using (var db = Context())
{
    var original = db.Records.Find(recordId)!;
    var copy = original with { };
    Check("record.equal-copy", original == copy && !ReferenceEquals(original, copy), "record == true, ReferenceEquals false");
    Conflict("same-key.record.equal-copy", () => db.Attach(copy));
}

RecordEntity detachedRecord;
ClassEntity detachedClass;
using (var db = Context())
{
    detachedRecord = db.Records.AsNoTracking().Single(x => x.Id == recordId);
    detachedClass = db.Classes.AsNoTracking().Single(x => x.Id == classId);
}
using (var db = Context())
{
    db.Update(detachedRecord with { Name = "detached-update" });
    db.Update(new ClassEntity { Id = detachedClass.Id, Name = "detached-update", GroupId = detachedClass.GroupId });
    Check("fresh-context.Update", db.SaveChanges() == 2, "record with-copy and manual class-copy each updated a row");
}
using (var db = Context())
    Check("fresh-context.Update.persist", db.Records.Find(recordId)!.Name == "detached-update" && db.Classes.Find(classId)!.Name == "detached-update", "both persisted");
using (var db = Context())
{
    db.Attach(detachedRecord with { Name = "attach-alone" });
    Check("fresh-context.Attach-alone", db.SaveChanges() == 0, "Attach uses copied values as original snapshot; zero writes");
}
using (var db = Context())
{
    var copy = detachedRecord with { Name = "attach-marked" };
    db.Attach(copy);
    db.Entry(copy).Property(x => x.Name).IsModified = true;
    Check("fresh-context.Attach-marked", db.SaveChanges() == 1, "marking Name modified updates record copy");
}
using (var db = Context())
    Check("fresh-context.Attach-marked.persist", db.Records.Find(recordId)!.Name == "attach-marked", "fresh context read attach-marked");
using (var db = Context())
{
    var original = db.Records.Find(recordId)!;
    var copy = original with { Name = "merged" };
    db.Entry(original).CurrentValues.SetValues(copy);
    Check("same-context.SetValues", db.SaveChanges() == 1 && ReferenceEquals(original, db.Records.Find(recordId)), "copied values applied to existing tracked instance");
}

// Navigation collections: equal transient records (Id=0) can collapse before EF sees both.
foreach (var referenceComparer in new[] { false, true })
{
    using var db = Context();
    var group = new GroupEntity();
    if (referenceComparer) group.Records = new HashSet<RecordEntity>(ReferenceEqualityComparer.Instance);
    var a = new RecordEntity { Name = "equal-transient" };
    var b = new RecordEntity { Name = "equal-transient" };
    group.Records.Add(a);
    var addedSecond = group.Records.Add(b);
    group.Classes.Add(new ClassEntity { Name = "equal-transient" });
    group.Classes.Add(new ClassEntity { Name = "equal-transient" });
    var before = group.Records.Count;
    db.Groups.Add(group);
    db.SaveChanges();
    var rows = db.Records.Count(x => x.GroupId == group.Id);
    var classRows = db.Classes.Count(x => x.GroupId == group.Id);
    var expected = referenceComparer ? 2 : 1;
    Check($"navigation.transient.{(referenceComparer ? "reference" : "default")}", before == expected && rows == expected && classRows == 2,
        $"second record Add={addedSecond}, records before EF={before}, record rows={rows}, class rows={classRows}");
}

// Already-persisted children: scalar mutation changes a synthesized record hash in a HashSet.
foreach (var referenceComparer in new[] { false, true })
{
    int groupId;
    using (var db = Context())
    {
        var group = new GroupEntity { Records = new HashSet<RecordEntity>(ReferenceEqualityComparer.Instance) };
        group.Records.Add(new RecordEntity { Name = "hash-before" });
        group.Classes.Add(new ClassEntity { Name = "hash-before" });
        db.Add(group); db.SaveChanges(); groupId = group.Id;
    }
    using (var db = Context())
    {
        var group = db.Groups.Find(groupId)!;
        if (referenceComparer) group.Records = new HashSet<RecordEntity>(ReferenceEqualityComparer.Instance);
        db.Entry(group).Collection(x => x.Records).Load();
        db.Entry(group).Collection(x => x.Classes).Load();
        var record = group.Records.Single();
        var entity = group.Classes.Single();
        var beforeHash = record.GetHashCode();
        var containsBefore = group.Records.Contains(record);
        // Choose a changed hash explicitly; string hashes are randomized per process.
        for (var i = 0; record.GetHashCode() == beforeHash; i++) record.Name = $"hash-after-{i}";
        entity.Name = "hash-after";
        var containsAfter = group.Records.Contains(record);
        var removed = group.Records.Remove(record);
        var classRemoved = group.Classes.Remove(entity);
        db.SaveChanges();
        var linkedRows = db.Records.Count(x => x.GroupId == groupId);
        Check($"navigation.mutate-remove.{(referenceComparer ? "reference" : "default")}",
            containsBefore && containsAfter == referenceComparer && removed == referenceComparer && classRemoved && linkedRows == (referenceComparer ? 0 : 1),
            $"contains before={containsBefore}, after={containsAfter}, Remove={removed}, class Remove={classRemoved}, remaining linked record rows={linkedRows}");
    }
}

// EF's state-manager lookup still finds a record after a scalar hash change.
using (var db = Context())
{
    var original = db.Records.Find(recordId)!;
    original.Name = "tracker-final";
    Check("tracker.reference-after-record-mutation", ReferenceEquals(original, db.Records.Find(recordId)) && ReferenceEquals(original, db.Entry(original).Entity),
        "Find and Entry still resolve the same mutated record instance");
    db.SaveChanges();
}
Console.WriteLine($"SUMMARY passed={passed} failed={failed}");
Environment.ExitCode = failed == 0 ? 0 : 1;

public sealed record RecordEntity
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public int? GroupId { get; set; }
}
public sealed class ClassEntity
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public int? GroupId { get; set; }
}
public sealed class GroupEntity
{
    public int Id { get; set; }
    public HashSet<RecordEntity> Records { get; set; } = [];
    public HashSet<ClassEntity> Classes { get; set; } = [];
}
public sealed class ExperimentContext(DbContextOptions<ExperimentContext> options) : DbContext(options)
{
    public DbSet<RecordEntity> Records => Set<RecordEntity>();
    public DbSet<ClassEntity> Classes => Set<ClassEntity>();
    public DbSet<GroupEntity> Groups => Set<GroupEntity>();
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<RecordEntity>().HasKey(x => x.Id);
        modelBuilder.Entity<ClassEntity>().HasKey(x => x.Id);
        modelBuilder.Entity<GroupEntity>().HasMany(x => x.Records).WithOne().HasForeignKey(x => x.GroupId);
        modelBuilder.Entity<GroupEntity>().HasMany(x => x.Classes).WithOne().HasForeignKey(x => x.GroupId);
    }
}
