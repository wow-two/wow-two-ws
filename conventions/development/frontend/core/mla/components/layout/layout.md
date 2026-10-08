# Layout

*Last updated: 2026-10-01*

> Which layout to reach for, and with what values — the application register over the SDK's `layout/` group.
> Use case — picking between two arrangements that both work, or fixing the value one carries here.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Components

| Component | Reach for it when |
|---|---|
| [AnchorLayout](anchorLayout.md) | a child pins to a corner of the box it already sits in |
| [AppShell](appShell.md) | one frame owns the app — header, sidebar, main, aside, footer |
| [AspectRatioLayout](aspectRatioLayout.md) | a media box has to hold its shape before the media loads |
| [BoxLayout](boxLayout.md) | a shell needs a class, and nothing here has to be arranged |
| [CanvasArea](canvasArea.md) | a diagram, map or board pans and zooms inside a fixed box |
| [CenterLayout](centerLayout.md) | one child sits in the middle of its parent on both axes |
| [ClusterLayout](clusterLayout.md) | a wrapping row reads as centred — hero CTAs, footer links |
| [ContainerLayout](containerLayout.md) | page content is capped at a readable width and centred |
| [ControlGroupField](controlGroupField.md) | a muted label binds to the control beside or above it |
| [DividerLayout](dividerLayout.md) | a rule separates two runs of content, plain or labelled |
| [FlexLayout](flexLayout.md) | a one-off flex line needs classes [StackLayout](stackLayout.md) cannot spell |
| [FrameLayout](frameLayout.md) | a bordered padded shell is wanted without card slots |
| [Grid](grid.md) | items line up on two axes, in equal tracks |
| [HStackLayout](hStackLayout.md) | the row is fixed at the import, never at the call site |
| [InlineLayout](inlineLayout.md) | small items flow from the leading edge and wrap |
| [Navbar](navbar.md) | a header bar is all the frame the page needs |
| [PullToRefreshLayout](pullToRefreshLayout.md) | a phone list refreshes on a drag past the top |
| [ResizablePanelsLayout](resizablePanelsLayout.md) | the reader drags the split between two panes |
| [ScrollArea](scrollArea.md) | one region scrolls while the page around it stays put |
| [Section](section.md) | a full-bleed band wraps a centred column |
| [SpacerLayout](spacerLayout.md) | one flex child has to push its siblings apart |
| [StackLayout](stackLayout.md) | children run down one axis with a gap between them |
| [SurfaceLayout](surfaceLayout.md) | a bare wrapper carries the fill, border and shadow recipe |
| [TwoColumnLayout](twoColumnLayout.md) | a fixed aside sits beside a column that takes the rest |
| [VStackLayout](vStackLayout.md) | the column is fixed at the import, for symmetry with [HStackLayout](hStackLayout.md) |
