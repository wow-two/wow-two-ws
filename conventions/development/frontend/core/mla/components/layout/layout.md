# Layout

*Last updated: 2026-09-10*

> Which layout to reach for, and with what values — the application register over the SDK's `layout/` group.
> Use case — picking between two arrangements that both work, or fixing the value one carries here.
> What a layout is → [layout](../../constructs/visual/layout.md).

## Components

| Component | Reach for it when |
|---|---|
| [AppShell](appShell.md) | one frame owns the app — header, sidebar, main, aside, footer |
| [AspectRatio](aspectRatio.md) | a media box has to hold its shape before the media loads |
| [Box](box.md) | a shell needs a class, and nothing here has to be arranged |
| [Center](center.md) | one child sits in the middle of its parent on both axes |
| [Cluster](cluster.md) | a wrapping row reads as centred — hero CTAs, footer links |
| [Container](container.md) | page content is capped at a readable width and centred |
| [ControlGroup](controlGroup.md) | a muted label binds to the control beside or above it |
| [Divider](divider.md) | a rule separates two runs of content, plain or labelled |
| [Flex](flex.md) | a one-off flex line needs classes [Stack](stack.md) cannot spell |
| [Frame](frame.md) | a bordered padded shell is wanted without card slots |
| [Grid](grid.md) | items line up on two axes, in equal tracks |
| [HStack](hStack.md) | the row is fixed at the import, never at the call site |
| [Inline](inline.md) | small items flow from the leading edge and wrap |
| [Navbar](navbar.md) | a header bar is all the frame the page needs |
| [Overlay](overlay.md) | a child pins to a corner of the box it already sits in |
| [PullToRefresh](pullToRefresh.md) | a phone list refreshes on a drag past the top |
| [ResizablePanels](resizablePanels.md) | the reader drags the split between two panes |
| [ScrollArea](scrollArea.md) | one region scrolls while the page around it stays put |
| [Section](section.md) | a full-bleed band wraps a centred column |
| [Spacer](spacer.md) | one flex child has to push its siblings apart |
| [Stack](stack.md) | children run down one axis with a gap between them |
| [Surface](surface.md) | a bare wrapper carries the fill, border and shadow recipe |
| [TwoColumn](twoColumn.md) | a fixed aside sits beside a column that takes the rest |
| [VStack](vStack.md) | the column is fixed at the import, for symmetry with [HStack](hStack.md) |
