using System.Reflection;
using System.Runtime.InteropServices;
using CloneApi = Force.DeepCloner.DeepClonerExtensions;

Console.WriteLine($"ENV runtime={RuntimeInformation.FrameworkDescription} arch={RuntimeInformation.ProcessArchitecture} cloner={typeof(CloneApi).Assembly.GetCustomAttribute<AssemblyInformationalVersionAttribute>()?.InformationalVersion}");
int passed = 0, failed = 0;
void Check(string name, bool ok)
{
    Console.WriteLine($"{(ok ? "PASS" : "FAIL")} {name}");
    if (ok) passed++; else failed++;
}
var shared = new Node { Name = "shared" };
var root = new Graph { First = shared, Second = shared, Derived = new DerivedData { Name = "base", Details = ["derived"] } };
root.Nodes.Add(shared);
root.Map.Add("HELLO", shared);
root.Tags.Add("Alpha");
root.IdentitySet.Add(shared);
root.IdentityMap.Add(shared, "value");
root.PrivateAdd(shared);
root.ReadOnlyNodes.Add(shared);
root.CaseMap.Add("CUSTOM", shared);
root.Next = root;
shared.Next = shared;
var constructors = Graph.ConstructorCalls;
var copy = CloneApi.DeepClone(root)!;
Check("record root copied", !ReferenceEquals(root, copy));
Check("runtime derived type preserved", copy.Derived is DerivedData);
Check("root self cycle preserved", ReferenceEquals(copy, copy.Next));
Check("nested cycle preserved", ReferenceEquals(copy.First, copy.First.Next));
Check("shared alias properties preserved", ReferenceEquals(copy.First, copy.Second));
Check("shared alias list preserved", ReferenceEquals(copy.First, copy.Nodes.Single()));
Check("shared alias dictionary preserved", ReferenceEquals(copy.First, copy.Map["hello"]));
Check("shared alias private field preserved", ReferenceEquals(copy.First, copy.PrivateGet()));
Check("shared alias get-only property preserved", ReferenceEquals(copy.First, copy.ReadOnlyNodes.Single()));
Check("private readonly field isolated", !ReferenceEquals(root.PrivateGet(), copy.PrivateGet()));
Check("init property nested state isolated", !ReferenceEquals(root.First, copy.First));
Check("get-only mutable list isolated", !ReferenceEquals(root.ReadOnlyNodes, copy.ReadOnlyNodes));
Check("constructor not rerun", Graph.ConstructorCalls == constructors);
Check("list isolated", !ReferenceEquals(root.Nodes, copy.Nodes));
Check("dictionary comparer behavior preserved", copy.Map.ContainsKey("hello") && copy.Map.Comparer.Equals("HELLO", "hello"));
Check("set comparer behavior preserved", copy.Tags.Contains("alpha") && !copy.Tags.Add("ALPHA"));
Check("reference set contains cloned key", copy.IdentitySet.Contains(copy.First));
Check("reference set excludes original key", !copy.IdentitySet.Contains(root.First));
Check("reference dictionary finds cloned key", copy.IdentityMap.TryGetValue(copy.First, out var value) && value == "value");
Check("reference dictionary excludes original key", !copy.IdentityMap.ContainsKey(root.First));
Check("custom comparer dictionary works", copy.CaseMap.ContainsKey("custom"));
Check("derived mutable member isolated", !ReferenceEquals(((DerivedData)root.Derived).Details, ((DerivedData)copy.Derived).Details));
copy.First.Name = "copy-only";
copy.Nodes.Add(new Node { Name = "extra" });
copy.ReadOnlyNodes.Add(new Node { Name = "read-only-extra" });
copy.PrivateAdd(new Node { Name = "private-extra" });
copy.Map.Add("new", new Node());
copy.Tags.Add("Beta");
((DerivedData)copy.Derived).Details.Add("copy-only");
Check("mutation leaves original graph intact", root.First.Name == "shared" && root.Nodes.Count == 1 && root.ReadOnlyNodes.Count == 1 && root.PrivateCount == 1 && root.Map.Count == 1 && root.Tags.Count == 1 && ((DerivedData)root.Derived).Details.Count == 1);

// No cycle: verifies whether alias preservation silently depends on graph-cycle analysis.
var plain = new PlainGraph { First = new PlainNode { Items = ["original"] } };
plain.Second = plain.First;
var plainCopy = CloneApi.DeepClone(plain)!;
Check("acyclic shared alias preserved", ReferenceEquals(plainCopy.First, plainCopy.Second));
Check("acyclic shared object isolated", !ReferenceEquals(plainCopy.First, plain.First));
plainCopy.First.Items.Add("copy-only");
Check("acyclic original isolated", plain.First.Items.Count == 1);
// Record-generated hash includes List identity even though record overrides GetHashCode.
var compositeKey = new CompositeKey(1, ["part"]);
var scalarKey = new ScalarKey(1, "part");
var keyed = new KeyGraph { Key = compositeKey, Scalar = scalarKey };
keyed.Set.Add(compositeKey);
keyed.Map.Add(compositeKey, "composite-value");
keyed.ScalarSet.Add(scalarKey);
keyed.ScalarMap.Add(scalarKey, "scalar-value");
var keyedCopy = CloneApi.DeepClone(keyed)!;
Check("record list-key alias preserved", ReferenceEquals(keyedCopy.Key, keyedCopy.Set.Single()) && ReferenceEquals(keyedCopy.Key, keyedCopy.Map.Keys.Single()));
Check("record list-key parts isolated", !ReferenceEquals(keyedCopy.Key.Parts, keyed.Key.Parts));
Check("record list-key set contains cloned key", keyedCopy.Set.Contains(keyedCopy.Key));
Check("record list-key dictionary finds cloned key", keyedCopy.Map.TryGetValue(keyedCopy.Key, out var compositeValue) && compositeValue == "composite-value");
Check("scalar record-key set contains cloned key", keyedCopy.ScalarSet.Contains(keyedCopy.Scalar));
Check("scalar record-key dictionary finds cloned key", keyedCopy.ScalarMap.TryGetValue(keyedCopy.Scalar, out var scalarValue) && scalarValue == "scalar-value");
Console.WriteLine($"SUMMARY passed={passed} failed={failed}");
Environment.ExitCode = failed == 0 ? 0 : 1;

public sealed record Graph
{
    public static int ConstructorCalls;
    public Graph() => ConstructorCalls++;
    private readonly List<Node> _privateNodes = [];
    public void PrivateAdd(Node node) => _privateNodes.Add(node);
    public Node PrivateGet() => _privateNodes[0];
    public int PrivateCount => _privateNodes.Count;
    public List<Node> ReadOnlyNodes { get; } = [];
    public Node First { get; init; } = new();
    public Node Second { get; init; } = new();
    public List<Node> Nodes { get; init; } = [];
    public Dictionary<string, Node> Map { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public HashSet<string> Tags { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public HashSet<Node> IdentitySet { get; init; } = new(ReferenceEqualityComparer.Instance);
    public Dictionary<Node, string> IdentityMap { get; init; } = new(ReferenceEqualityComparer.Instance);
    public Dictionary<string, Node> CaseMap { get; init; } = new(new CaseComparer());
    public BaseData Derived { get; init; } = new();
    public Graph? Next { get; set; }
}
public sealed class Node { public string Name { get; set; } = ""; public Node? Next { get; set; } }
public class BaseData { public string Name { get; set; } = ""; }
public sealed class DerivedData : BaseData { public List<string> Details { get; init; } = []; }
public sealed record PlainGraph { public PlainNode First { get; init; } = new(); public PlainNode Second { get; set; } = new(); }
public sealed class PlainNode { public List<string> Items { get; init; } = []; }
public sealed class CaseComparer : IEqualityComparer<string>
{
    public bool Equals(string? x, string? y) => StringComparer.OrdinalIgnoreCase.Equals(x, y);
    public int GetHashCode(string value) => StringComparer.OrdinalIgnoreCase.GetHashCode(value);
}

public sealed record CompositeKey(int Id, List<string> Parts);
public sealed record ScalarKey(int Id, string Part);
public sealed record KeyGraph
{
    public CompositeKey Key { get; init; } = new(0, []);
    public ScalarKey Scalar { get; init; } = new(0, "");
    public HashSet<CompositeKey> Set { get; init; } = [];
    public Dictionary<CompositeKey, string> Map { get; init; } = [];
    public HashSet<ScalarKey> ScalarSet { get; init; } = [];
    public Dictionary<ScalarKey, string> ScalarMap { get; init; } = [];
}
