# fastcloner copy experiment

Isolated .NET 10 graph-copy checks. Run `dotnet run --project experiment.csproj` from this directory.

Verified 2026-09-13: package 3.5.6, .NET 10.0.8 Arm64; **32 passed, 0 failed**, exit 0.
Native escalation resolved the official NuGet restore restriction; execution ran normally afterward.
The executed temporary source matches this directory's `Program.cs` byte-for-byte.
[Full output](results.txt). SDK integration remains separate.

[Library comparison and verification status](../../deep-copy-analysis.md).
