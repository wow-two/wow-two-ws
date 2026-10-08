# Feedback

*Last updated: 2026-10-01*

> Which report to reach for, and with what values — the application register over the SDK's `feedback/` group.
> Use case — picking between two reports that both work, or fixing the value one carries here.
> What a feedback component is → [feedback](../../constructs/visual/feedback.md).

## Components

| Component | Reach for it when |
|---|---|
| [Alert](alert.md) | a section-level note carries a title, a body, and actions |
| [AlertSimple](alertSimple.md) | the note's tinted surface is wanted around free-form children |
| [Banner](banner.md) | the condition affects the whole app and pins across the top |
| [BannerSimple](bannerSimple.md) | the pinned strip takes free-form children |
| [Callout](callout.md) | a doc-style aside sits inline in prose, quieter than an alert |
| [FeedbackToastHost](feedbackToastHost.md) | toasts come from the headless `notify()` bus |
| [InlineSpinner](inlineSpinner.md) | a busy mark sits mid-flow with a word beside it |
| [LiveCursorIndicator](liveCursorIndicator.md) | a collaborator's pointer is drawn on a shared surface |
| [LoadingOverlay](loadingOverlay.md) | a region stays visible but must stop answering |
| [LoadingState](loadingState.md) | a whole section is waiting and centres its report |
| [MeterBar](meterBar.md) | a level changes tone as it crosses its thresholds |
| [NotificationCenterGroup](notificationCenterGroup.md) | past notices are browsed in a panel |
| [OnboardingChecklistCard](onboardingChecklistCard.md) | first-run tasks are tracked to completion |
| [PresenceIndicator](presenceIndicator.md) | one person's connection state reads as a dot |
| [ProgressBar](progressBar.md) | a task's completion reads left to right |
| [ProgressCircleIndicator](progressCircleIndicator.md) | that same completion has to fit a square |
| [ProgressStepsIndicator](progressStepsIndicator.md) | a flow's named stages show which one is current |
| [SkeletonState](skeletonState.md) | the shape of unloaded content stands in for it |
| [Spinner](spinner.md) | a bare indeterminate mark is the whole report |
| [SplashScreen](splashScreen.md) | the app's first load shows the product logo over a progress bar |
| [StatusIndicator](statusIndicator.md) | a service's health reads as a dot plus a line |
| [Toast](toast.md) | one transient card is mounted by hand, outside the queue |
| [ToastHost](toastHost.md) | the app fires toasts imperatively from anywhere |
| [ToastSimple](toastSimple.md) | the transient card takes free-form children |
| [TrendIndicator](trendIndicator.md) | a metric's delta reads as a signed arrow |
| [TypingIndicator](typingIndicator.md) | someone is composing a message right now |
| [UndoBar](undoBar.md) | a destructive act stays reversible for a few seconds |

---

## Loading

Which surface answers which wait; the linked owner states the values.

| The wait | Surface | Owner |
|---|---|---|
| the app's first load, before the shell renders | `SplashScreen` | [SplashScreen](splashScreen.md) |
| a route's chunk loading | the router's loading outcome | [routing](../../../../shapes/app/routing/routing.md#places) |
| a region's first load, shape known | `SkeletonState` | [loading](../../domains/data/state-and-data.md#loading) |
| a region's first load, shape unknown | `LoadingState` | [LoadingState](loadingState.md) |
| a refresh the user asked for | `SkeletonStateGroup` + `useRefresh` | [loading](../../domains/data/state-and-data.md#loading) |
| a background refetch or poll | none — content stays, freshness shows | [loading](../../domains/data/state-and-data.md#loading) |
| one command in flight | `Button` `isLoading` | [Button](../actions/button.md) |
| a busy mark inside a row or a sentence | `InlineSpinner` | [InlineSpinner](inlineSpinner.md) |
| a long task that must not be repeated or interleaved | `LoadingOverlay` | [LoadingOverlay](loadingOverlay.md) |
