var entity = new Row { Id = 1, Name = "A", Secret = "synthetic-secret" };
var equalCopy = entity with { };
Check("same values equal; instances distinct", entity == equalCopy && !ReferenceEquals(entity, equalCopy));
var candidate = entity with { Name = "B" };
Check("with preserves original scalar", entity.Name == "A" && candidate.Name == "B");
candidate.Tags.Add("shared");
Check("with shares reference members", entity.Tags.Contains("shared") && ReferenceEquals(entity.Tags, candidate.Tags));
Check("same key different state unequal", entity.Id == candidate.Id && entity != candidate);
var set = new HashSet<Row> { entity };
var originalHash = entity.GetHashCode();
entity.Name = "changed";
Check("mutated record default hash lookup fails in sample", entity.GetHashCode() != originalHash && !set.Contains(entity));
var identitySet = new HashSet<Row>(ReferenceEqualityComparer.Instance) { entity };
entity.Name = "changed-again";
Check("reference comparer survives state mutation", identitySet.Contains(entity));
var classRow = new PlainRow { Id = 1, Name = "A" };
var classSet = new HashSet<PlainRow> { classRow };
classRow.Name = "B";
Check("plain class default hash lookup survives mutation", classSet.Contains(classRow));
Check("separate list contents not structural equality", new Row { Id = 1, Name = "A" } != new Row { Id = 1, Name = "A" });
Check("generated ToString includes public secret", entity.ToString().Contains("synthetic-secret"));
var validRange = new RangeValue(1, 5);
var invalidCopy = validRange with { Start = 10 };
Check("with bypasses original constructor relation check", invalidCopy.Start > invalidCopy.End);
Console.WriteLine("10/10 checks passed");
static void Check(string label, bool actual) { if (!actual) throw new Exception(label); Console.WriteLine("PASS " + label); }
sealed record Row { public int Id { get; set; } public string Name { get; set; } = ""; public string Secret { get; set; } = ""; public List<string> Tags { get; init; } = []; }
sealed class PlainRow { public int Id { get; set; } public string Name { get; set; } = ""; }
sealed record RangeValue { public int Start { get; init; } public int End { get; init; } public RangeValue(int start, int end) { if (start > end) throw new ArgumentException("range"); Start = start; End = end; } }
