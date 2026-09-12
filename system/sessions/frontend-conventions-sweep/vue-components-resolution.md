# Vue presentation conventions sweep resolution

## Status

- Naming/classification, specifications, typed gallery fixtures and the bounded presentation behavior fixes are implemented.
- No convention design decision remains in this lane. Final package gates and publishing remain with the coordinating task.
- This is source/API coverage and named regression evidence; render tests do not establish every interaction in every specification.

## Scope and coverage

SDK: `/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk`.

| Inventory | Expected | Actual | Evidence |
|---|---:|---:|---|
| Adjacent SFC specifications | 379 | 379 | Every source SFC has its own props, emits, slots, exposed handle and behavioral contract |
| Directly indexed public SFC exports with typed fixtures | 349 | 349 | Shared seven-group example registry; no missing public SFC fixture |
| SFC-named fixtures including additional reexports | 356 | 356 | Remaining 23 implementation parts are composed through their family |
| New specifications added | 199 | 199 | The 180 existing specifications were refreshed against Vue source |
| Root families explicitly classified/renamed or moved | 109 | 109 | Full mapping below |
| Native reset integrations | 54 | 54 | 20 direct native controls; 31 stateful composite roots; 3 caller-controlled emoji roots |
| Broken local specification links | 0 | 0 | All 379 documents checked |
| React-era references in current specifications | 0 | 0 | Source surface uses Vue imports, events and slots |

## Resolved sweep rows

| Row | Resolution |
|---|---|
| 7, 25 | Root kind suffixes, semantic group placement, prefixed compound parts, barrels and owned source/test/demo references updated. Native tags, browser Image and semantic enum members retained. |
| 8, 18, 27 | All SFC specs rebuilt from actual declarations and contracts; typed fixtures shared between tests and playground. Curated examples preserved. Auto gallery mounts required context and props; guard failures are visible errors. Native navigation links select gallery groups. |
| 33 | Modal/Drawer/BottomSheet opt into FocusScope modal behavior. Popover is nonmodal by default, trapping and aria-modal follow explicit isModal. Actual keyboard focus scenarios authored for the browser gate. |
| 34 | CodeEditor advertises Escape then Tab/Shift+Tab exit and supports native Tab mode. TagsInput commits on Tab without trapping it. Marquee, Typewriter, Carousel and animated GradientText expose persistent pause controls. Marquee duplicate is inert. Carousel autoplay is mount-only and respects reduced motion, focus and hover independently. |
| 34 | SortableGroupMoveButton provides bounded single-pointer reorder actions. NodeEditor has node selection/movement buttons, focused-node arrow movement and keyboard edge activation; inner controls do not start dragging. |
| 35 | Shared state owner is fixed at setup (foundation lane). IME guards prevent premature transforms/commits. NumberInput commits number or null and honors readonly steppers. Reset runs once at the composite owner and refreshes nested native representation. |
| 37 | Unambiguous legacy important modifiers normalized to Tailwind trailing !; parent focus-outline edits preserved. |
| 40 | Markdown raw HTML remains escaped; default preview URL policy uses shared UrlExtensions. LinkItem/Breadcrumb navigation and PDF/image/audio/video source bindings select safe schemes. Custom preview/router slots remain caller-owned. |

## Reset contract and evidence

- Composite reset anchors are hidden native inputs with no name, so they join native form association without submitting a value. Explicit form IDs are forwarded to the anchor.
- A provided reset scope suppresses nested child default requests when the outer component owns the same form; this prevents children overwriting restored group selections.
- Controlled reset requests the original seed/clear but does not replace caller state. Uncontrolled reset restores its initial seed.
- Composite revision changes remount local drafts from resolved state. Focus restoration uses stable control attributes and the ordinal among equivalent controls, so removed tag buttons do not shift a text input. Stable IDs take precedence. The HTMLElement check uses the target owner document.
- Cancelled resets do nothing. The queued callback rechecks native form association and mount state before resetting and before reconciliation.
- Five focused tests cover one reset for uncontrolled/controlled checkbox groups, tag value plus unfinished draft, PIN cells, and toggle selection. Focus assertions cover a PIN cell and TagsInput with an extra committed chip removed by reset.
- Navigation-only WizardForm step state is not a form value. FilePicker/FileUploadPicker dispatch file selection actions; they do not own a committed model to reseed. Their native file elements follow browser reset.

## Verification checkpoint

| Check | Result | Evidence |
|---|---|
| Presentation DOM + SSR suite | 30 files, 1,096 tests passed | `/private/tmp/vue-lane-final4-tests.log` |
| Focus-preserving composite reset | 5 tests passed, includes removed tag chips and PIN focus | `/private/tmp/vue-composite-reset-focus.log` |
| Source/test typecheck | Presentation/test scope clean at checkpoint; later shared TanStack changes were in flight | `/private/tmp/vue-lane-final4-types.log` |
| Playground typecheck | Passed | `/private/tmp/vue-lane-playground-final2.log` |
| SFC compile | 407 SFCs compile across package | `/private/tmp/vue-lane-sfc-final2.log` |
| Scoped lint | Passed with zero errors or warnings | `/private/tmp/vue-lane-hold-lint.log` |
| Scoped format / diff whitespace | Formatter applied; diff --check passed | `/private/tmp/vue-lane-hold-format.log` |
| Specifications/local links | 379/379 present, zero broken links | Checked after all spec writes |
| Browser focus tests | Authored; local runner blocked before any tests executed by listen EPERM on ::1 | `/private/tmp/vue-keyboard-browser.log` |

The parent owns the final aggregate rerun after foundation/forms imports settle. Format was applied only inside this lane; no staging, commit, version bump or publish occurred here.

## Browser acceptance still to execute

- `/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/tests/unit/presentation/forms/KeyboardExit.browser.test.ts`: CodeEditor Escape then Tab leaves; each breadcrumb ancestor remains in Tab order; nonmodal Popover permits focus to leave.
- Existing modal nesting, forced-colors focus and foundation owner-document tests remain part of the coordinating browser gate.
- Manual gallery review should inspect all seven group links, composed examples, localized action labels and narrow layouts. This lane does not claim those visual checks ran.

## Root mapping

| Previous root | Current root | Current group |
|---|---|---|
| `Accordion` | `AccordionGroup` | `display` |
| `ActivityFeed` | `ActivityTimeline` | `display` |
| `AddressForm` | `AddressEditor` | `forms` |
| `AnimatedNumber` | `AnimatedNumberText` | `display` |
| `AnnotationMarker` | `AnnotationBadge` | `display` |
| `AspectRatio` | `AspectRatioLayout` | `layout` |
| `AudioWaveform` | `AudioWaveformPreview` | `display` |
| `Backdrop` | `BackdropOverlay` | `overlays` |
| `Box` | `BoxLayout` | `layout` |
| `Calendar` | `CalendarPicker` | `forms` |
| `Center` | `CenterLayout` | `layout` |
| `CharacterCount` | `CharacterCountCallout` | `feedback` |
| `ChatBubble` | `ChatBubbleCard` | `display` |
| `ChatComposer` | `ChatComposerInput` | `forms` |
| `Checkbox` | `CheckboxInput` | `forms` |
| `Cluster` | `ClusterLayout` | `layout` |
| `Code` | `CodeText` | `display` |
| `Collapsible` | `CollapsibleGroup` | `display` |
| `ColorSlider` | `ColorSliderInput` | `forms` |
| `ColorSwatch` | `ColorSwatchPreview` | `display` |
| `ColorWheel` | `ColorWheelInput` | `forms` |
| `Combobox` | `ComboboxPicker` | `forms` |
| `CommandPalette` | `CommandPaletteModal` | `overlays` |
| `CommentThread` | `CommentThreadGroup` | `display` |
| `Confetti` | `ConfettiOverlay` | `display` |
| `Container` | `ContainerLayout` | `layout` |
| `ControlGroup` | `ControlGroupField` | `forms` |
| `CountUp` | `CountUpText` | `display` |
| `DataGrid` | `DataGridEditor` | `forms` |
| `DescriptionList` | `DescriptionGroup` | `display` |
| `Divider` | `DividerLayout` | `layout` |
| `Editable` | `EditableInput` | `forms` |
| `EmojiSizeControl` | `EmojiSizePicker` | `forms` |
| `EventCalendar` | `EventCalendarViewer` | `display` |
| `Eyebrow` | `EyebrowText` | `display` |
| `Fab` | `FabButton` | `actions` |
| `Fieldset` | `FieldsetLayout` | `layout` |
| `FileUpload` | `FileUploadPicker` | `forms` |
| `Flex` | `FlexLayout` | `layout` |
| `FormErrorMessage` | `FieldErrorCallout` | `feedback` |
| `FormHelperText` | `FieldHelperText` | `display` |
| `Frame` | `FrameLayout` | `layout` |
| `Gantt` | `GanttTimeline` | `display` |
| `HStack` | `HStackLayout` | `layout` |
| `HeatmapCalendar` | `HeatmapCalendarGrid` | `display` |
| `Highlight` | `HighlightText` | `display` |
| `Image` | `ImagePreview` | `display` |
| `Inline` | `InlineLayout` | `layout` |
| `InputAddon` | `InputAddonLayout` | `layout` |
| `InputGroup` | `InputGroup` | `layout` |
| `Kbd` | `KbdText` | `display` |
| `KeyboardShortcut` | `KeyboardShortcutText` | `display` |
| `Knob` | `KnobInput` | `forms` |
| `Label` | `LabelText` | `display` |
| `LabeledInput` | `LabeledField` | `forms` |
| `Legend` | `LegendText` | `display` |
| `Link` | `LinkItem` | `nav` |
| `List` | `ListGroup` | `display` |
| `Listbox` | `ListboxPicker` | `forms` |
| `LiveCursor` | `LiveCursorIndicator` | `feedback` |
| `Mark` | `MarkText` | `display` |
| `Marquee` | `MarqueeGroup` | `display` |
| `MessageList` | `MessageGroup` | `display` |
| `MetaInline` | `MetaInlineText` | `display` |
| `MetricChip` | `MetricBadge` | `display` |
| `MultiSelect` | `MultiSelectPicker` | `forms` |
| `NodeEditor` | `NodeEditor` | `forms` |
| `NotificationCenter` | `NotificationCenterGroup` | `display` |
| `NotificationDot` | `NotificationIndicator` | `display` |
| `OnboardingChecklist` | `OnboardingChecklistCard` | `display` |
| `OptionTile` | `OptionTilePicker` | `forms` |
| `OptionTileGroup` | `OptionTileGroupField` | `forms` |
| `Overlay` | `AnchorLayout` | `layout` |
| `PasswordStrength` | `PasswordStrengthCallout` | `feedback` |
| `ProgressCircle` | `ProgressCircleIndicator` | `feedback` |
| `ProgressSteps` | `ProgressStepsIndicator` | `feedback` |
| `PullToRefresh` | `PullToRefreshLayout` | `layout` |
| `Quote` | `QuoteText` | `display` |
| `Radio` | `RadioInput` | `forms` |
| `RangeCalendar` | `RangeCalendarPicker` | `forms` |
| `ResizablePanels` | `ResizablePanelsLayout` | `layout` |
| `ScrollReveal` | `ScrollRevealGroup` | `display` |
| `SectionHeader` | `SectionHeading` | `display` |
| `SegmentedControl` | `SegmentedPicker` | `forms` |
| `Select` | `SelectPicker` | `forms` |
| `Separator` | `SeparatorLayout` | `layout` |
| `Skeleton` | `SkeletonState` | `feedback` |
| `Slider` | `SliderInput` | `forms` |
| `Snippet` | `SnippetText` | `display` |
| `Sortable` | `SortableGroup` | `forms` |
| `Spacer` | `SpacerLayout` | `layout` |
| `SpeedDial` | `SpeedDialGroup` | `actions` |
| `Stack` | `StackLayout` | `layout` |
| `Stat` | `StatCard` | `display` |
| `Stepper` | `StepperGroup` | `display` |
| `Surface` | `SurfaceLayout` | `layout` |
| `SwipeActions` | `SwipeActionsLayout` | `layout` |
| `Switch` | `SwitchInput` | `forms` |
| `Tabs` | `TabsGroup` | `display` |
| `Tilt` | `TiltLayout` | `layout` |
| `ToggleButton` | `ToggleInput` | `forms` |
| `ToggleButtonGroup` | `ToggleGroup` | `forms` |
| `Tooltip` | `Tooltip` | `overlays` |
| `Tour` | `TourPopover` | `overlays` |
| `Tree` | `TreeViewer` | `display` |
| `TwoColumn` | `TwoColumnLayout` | `layout` |
| `Typewriter` | `TypewriterText` | `display` |
| `VStack` | `VStackLayout` | `layout` |
| `Wizard` | `WizardForm` | `forms` |

## Complete SFC/spec coverage

Every source path below has an adjacent `.spec.md`. `public` means exported directly by its family index; `fixture` means an independently named typed example. Internal parts without an independent fixture render through their owning family.

| Source relative to SDK | Public | Fixture |
|---|---|---|
| `src/presentation/actions/backToTopButton/BackToTopButton.vue` | yes | yes |
| `src/presentation/actions/button/Button.vue` | yes | yes |
| `src/presentation/actions/buttonGroup/ButtonGroup.vue` | yes | yes |
| `src/presentation/actions/copyButton/CopyButton.vue` | yes | yes |
| `src/presentation/actions/disclosureButton/DisclosureButton.vue` | yes | yes |
| `src/presentation/actions/fabButton/FabButton.vue` | yes | yes |
| `src/presentation/actions/googleSignInButton/GoogleSignInButton.vue` | yes | yes |
| `src/presentation/actions/speedDialGroup/SpeedDialGroup.vue` | internal/reexport | yes |
| `src/presentation/actions/speedDialGroup/SpeedDialGroupAction.vue` | internal/reexport | yes |
| `src/presentation/actions/speedDialGroup/SpeedDialGroupList.vue` | internal/reexport | family composition |
| `src/presentation/actions/speedDialGroup/SpeedDialGroupTrigger.vue` | internal/reexport | yes |
| `src/presentation/actions/toolbar/Toolbar.vue` | internal/reexport | yes |
| `src/presentation/actions/toolbar/ToolbarButton.vue` | internal/reexport | yes |
| `src/presentation/actions/toolbar/ToolbarLink.vue` | internal/reexport | yes |
| `src/presentation/actions/toolbar/ToolbarSeparator.vue` | internal/reexport | yes |
| `src/presentation/display/accordionGroup/AccordionGroup.vue` | yes | yes |
| `src/presentation/display/accordionGroup/AccordionGroupContent.vue` | yes | yes |
| `src/presentation/display/accordionGroup/AccordionGroupItem.vue` | yes | yes |
| `src/presentation/display/accordionGroup/AccordionGroupTrigger.vue` | yes | yes |
| `src/presentation/display/activityTimeline/ActivityItem.vue` | yes | yes |
| `src/presentation/display/activityTimeline/ActivityTimeline.vue` | yes | yes |
| `src/presentation/display/animatedNumberText/AnimatedNumberText.vue` | yes | yes |
| `src/presentation/display/annotationBadge/AnnotationBadge.vue` | yes | yes |
| `src/presentation/display/audioPlayer/AudioPlayer.vue` | yes | yes |
| `src/presentation/display/audioWaveformPreview/AudioWaveformPreview.vue` | yes | yes |
| `src/presentation/display/avatar/Avatar.vue` | yes | yes |
| `src/presentation/display/avatarGroup/AvatarGroup.vue` | yes | yes |
| `src/presentation/display/badge/Badge.vue` | yes | yes |
| `src/presentation/display/badgeOverlay/BadgeOverlay.vue` | yes | yes |
| `src/presentation/display/card/Card.vue` | yes | yes |
| `src/presentation/display/card/CardBody.vue` | yes | yes |
| `src/presentation/display/card/CardDescription.vue` | yes | yes |
| `src/presentation/display/card/CardFooter.vue` | yes | yes |
| `src/presentation/display/card/CardHeader.vue` | yes | yes |
| `src/presentation/display/card/CardTitle.vue` | yes | yes |
| `src/presentation/display/carousel/Carousel.vue` | yes | yes |
| `src/presentation/display/carousel/CarouselDot.vue` | yes | yes |
| `src/presentation/display/carousel/CarouselDots.vue` | yes | yes |
| `src/presentation/display/carousel/CarouselNext.vue` | yes | yes |
| `src/presentation/display/carousel/CarouselPrev.vue` | yes | yes |
| `src/presentation/display/carousel/CarouselSlide.vue` | yes | yes |
| `src/presentation/display/carousel/CarouselSlides.vue` | yes | yes |
| `src/presentation/display/carousel/CarouselViewport.vue` | yes | yes |
| `src/presentation/display/chatBubbleCard/ChatBubbleCard.vue` | yes | yes |
| `src/presentation/display/codeText/CodeText.vue` | yes | yes |
| `src/presentation/display/collapsibleGroup/CollapsibleGroup.vue` | yes | yes |
| `src/presentation/display/collapsibleGroup/CollapsibleGroupContent.vue` | yes | yes |
| `src/presentation/display/collapsibleGroup/CollapsibleGroupContentInner.vue` | internal/reexport | family composition |
| `src/presentation/display/collapsibleGroup/CollapsibleGroupTrigger.vue` | yes | yes |
| `src/presentation/display/colorSwatchPreview/ColorSwatchPreview.vue` | yes | yes |
| `src/presentation/display/commentThreadGroup/Comment.vue` | yes | yes |
| `src/presentation/display/commentThreadGroup/CommentThreadGroup.vue` | yes | yes |
| `src/presentation/display/confettiOverlay/ConfettiOverlay.vue` | yes | yes |
| `src/presentation/display/countBadge/CountBadge.vue` | yes | yes |
| `src/presentation/display/countUpText/CountUpText.vue` | yes | yes |
| `src/presentation/display/dataTable/DataTable.vue` | yes | yes |
| `src/presentation/display/descriptionGroup/DescriptionGroup.vue` | yes | yes |
| `src/presentation/display/diffViewer/DiffViewer.vue` | yes | yes |
| `src/presentation/display/emptyState/EmptyState.vue` | yes | yes |
| `src/presentation/display/eventCalendarViewer/AgendaView.vue` | internal/reexport | family composition |
| `src/presentation/display/eventCalendarViewer/EventCalendarViewer.vue` | yes | yes |
| `src/presentation/display/eventCalendarViewer/MonthView.vue` | internal/reexport | family composition |
| `src/presentation/display/eventCalendarViewer/TimeGridView.vue` | internal/reexport | family composition |
| `src/presentation/display/eyebrowText/EyebrowText.vue` | yes | yes |
| `src/presentation/display/featureCard/FeatureCard.vue` | yes | yes |
| `src/presentation/display/fieldHelperText/FieldHelperText.vue` | yes | yes |
| `src/presentation/display/frameGlyph/FrameGlyph.vue` | yes | yes |
| `src/presentation/display/ganttTimeline/GanttTimeline.vue` | yes | yes |
| `src/presentation/display/gradientText/GradientText.vue` | yes | yes |
| `src/presentation/display/heading/Heading.vue` | yes | yes |
| `src/presentation/display/heatmapCalendarGrid/HeatmapCalendarGrid.vue` | yes | yes |
| `src/presentation/display/highlightText/HighlightText.vue` | yes | yes |
| `src/presentation/display/imagePreview/ImagePreview.vue` | yes | yes |
| `src/presentation/display/infoRow/InfoRow.vue` | yes | yes |
| `src/presentation/display/kbdText/KbdText.vue` | yes | yes |
| `src/presentation/display/keyboardShortcutText/KeyboardShortcutText.vue` | yes | yes |
| `src/presentation/display/labelText/LabelText.vue` | yes | yes |
| `src/presentation/display/legendText/LegendText.vue` | yes | yes |
| `src/presentation/display/listGroup/ListGroup.vue` | yes | yes |
| `src/presentation/display/listGroup/ListGroupItem.vue` | yes | yes |
| `src/presentation/display/markText/MarkText.vue` | yes | yes |
| `src/presentation/display/marqueeGroup/MarqueeGroup.vue` | yes | yes |
| `src/presentation/display/messageGroup/DaySeparator.vue` | yes | yes |
| `src/presentation/display/messageGroup/MessageGroup.vue` | yes | yes |
| `src/presentation/display/metaInlineText/MetaInlineText.vue` | yes | yes |
| `src/presentation/display/metricBadge/MetricBadge.vue` | yes | yes |
| `src/presentation/display/moduleGlyphs/CellsGlyph.vue` | yes | yes |
| `src/presentation/display/moduleGlyphs/DotsGlyph.vue` | yes | yes |
| `src/presentation/display/moduleGlyphs/HorizontalBarsGlyph.vue` | yes | yes |
| `src/presentation/display/moduleGlyphs/VerticalBarsGlyph.vue` | yes | yes |
| `src/presentation/display/notificationCenterGroup/NotificationCenterGroup.vue` | yes | yes |
| `src/presentation/display/notificationCenterGroup/NotificationItem.vue` | yes | yes |
| `src/presentation/display/notificationIndicator/NotificationIndicator.vue` | yes | yes |
| `src/presentation/display/onboardingChecklistCard/OnboardingChecklistCard.vue` | yes | yes |
| `src/presentation/display/onboardingChecklistCard/OnboardingChecklistCardTask.vue` | yes | yes |
| `src/presentation/display/pdfViewer/PdfViewer.vue` | yes | yes |
| `src/presentation/display/pricingCard/PricingCard.vue` | yes | yes |
| `src/presentation/display/quoteText/QuoteText.vue` | yes | yes |
| `src/presentation/display/radiusGlyph/RadiusGlyph.vue` | yes | yes |
| `src/presentation/display/reactionBar/ReactionBar.vue` | yes | yes |
| `src/presentation/display/scheduleView/ScheduleView.vue` | yes | yes |
| `src/presentation/display/scrollRevealGroup/ScrollRevealGroup.vue` | yes | yes |
| `src/presentation/display/sectionHeading/SectionHeading.vue` | yes | yes |
| `src/presentation/display/snippetText/SnippetText.vue` | yes | yes |
| `src/presentation/display/sparkline/Sparkline.vue` | yes | yes |
| `src/presentation/display/statCard/StatCard.vue` | yes | yes |
| `src/presentation/display/status/Status.vue` | yes | yes |
| `src/presentation/display/stepCard/StepCard.vue` | yes | yes |
| `src/presentation/display/stepperGroup/StepperGroup.vue` | yes | yes |
| `src/presentation/display/stepperGroup/StepperGroupList.vue` | yes | yes |
| `src/presentation/display/stepperGroup/StepperGroupPanel.vue` | yes | yes |
| `src/presentation/display/stepperGroup/StepperGroupStep.vue` | yes | yes |
| `src/presentation/display/table/Table.vue` | yes | yes |
| `src/presentation/display/table/TableBody.vue` | yes | yes |
| `src/presentation/display/table/TableCaption.vue` | yes | yes |
| `src/presentation/display/table/TableCell.vue` | yes | yes |
| `src/presentation/display/table/TableFooter.vue` | yes | yes |
| `src/presentation/display/table/TableHead.vue` | yes | yes |
| `src/presentation/display/table/TableHeaderCell.vue` | yes | yes |
| `src/presentation/display/table/TableRow.vue` | yes | yes |
| `src/presentation/display/tabsGroup/TabsGroup.vue` | yes | yes |
| `src/presentation/display/tabsGroup/TabsGroupList.vue` | yes | yes |
| `src/presentation/display/tabsGroup/TabsGroupPanel.vue` | yes | yes |
| `src/presentation/display/tabsGroup/TabsGroupTab.vue` | yes | yes |
| `src/presentation/display/tag/Tag.vue` | yes | yes |
| `src/presentation/display/text/Text.vue` | yes | yes |
| `src/presentation/display/threadView/ThreadView.vue` | yes | yes |
| `src/presentation/display/timeline/Timeline.vue` | yes | yes |
| `src/presentation/display/timeline/TimelineDescription.vue` | yes | yes |
| `src/presentation/display/timeline/TimelineItem.vue` | yes | yes |
| `src/presentation/display/timeline/TimelineTitle.vue` | yes | yes |
| `src/presentation/display/treeViewer/TreeViewer.vue` | yes | yes |
| `src/presentation/display/treeViewer/TreeViewerGroup.vue` | yes | yes |
| `src/presentation/display/treeViewer/TreeViewerGroupContent.vue` | internal/reexport | family composition |
| `src/presentation/display/treeViewer/TreeViewerItem.vue` | yes | yes |
| `src/presentation/display/treeViewer/TreeViewerNodeRow.vue` | internal/reexport | family composition |
| `src/presentation/display/typewriterText/TypewriterText.vue` | yes | yes |
| `src/presentation/display/videoPlayer/VideoPlayer.vue` | yes | yes |
| `src/presentation/feedback/alert/Alert.vue` | yes | yes |
| `src/presentation/feedback/alertSimple/AlertSimple.vue` | yes | yes |
| `src/presentation/feedback/banner/Banner.vue` | yes | yes |
| `src/presentation/feedback/bannerSimple/BannerSimple.vue` | yes | yes |
| `src/presentation/feedback/callout/Callout.vue` | yes | yes |
| `src/presentation/feedback/characterCountCallout/CharacterCountCallout.vue` | yes | yes |
| `src/presentation/feedback/feedbackToastHost/FeedbackToastHost.vue` | yes | yes |
| `src/presentation/feedback/fieldErrorCallout/FieldErrorCallout.vue` | yes | yes |
| `src/presentation/feedback/inlineSpinner/InlineSpinner.vue` | yes | yes |
| `src/presentation/feedback/liveCursorIndicator/LiveCursorIndicator.vue` | yes | yes |
| `src/presentation/feedback/loadingOverlay/LoadingOverlay.vue` | yes | yes |
| `src/presentation/feedback/loadingState/LoadingState.vue` | yes | yes |
| `src/presentation/feedback/meterBar/MeterBar.vue` | yes | yes |
| `src/presentation/feedback/passwordStrengthCallout/PasswordStrengthCallout.vue` | yes | yes |
| `src/presentation/feedback/presenceIndicator/PresenceIndicator.vue` | yes | yes |
| `src/presentation/feedback/progressBar/ProgressBar.vue` | yes | yes |
| `src/presentation/feedback/progressCircleIndicator/ProgressCircleIndicator.vue` | yes | yes |
| `src/presentation/feedback/progressStepsIndicator/ProgressStepsIndicator.vue` | yes | yes |
| `src/presentation/feedback/skeletonState/SkeletonState.vue` | yes | yes |
| `src/presentation/feedback/spinner/Spinner.vue` | yes | yes |
| `src/presentation/feedback/statusIndicator/StatusIndicator.vue` | yes | yes |
| `src/presentation/feedback/toast/Toast.vue` | yes | yes |
| `src/presentation/feedback/toastHost/ToastHost.vue` | yes | yes |
| `src/presentation/feedback/toastSimple/ToastSimple.vue` | yes | yes |
| `src/presentation/feedback/trendIndicator/TrendIndicator.vue` | yes | yes |
| `src/presentation/feedback/typingIndicator/TypingIndicator.vue` | yes | yes |
| `src/presentation/feedback/undoBar/UndoBar.vue` | yes | yes |
| `src/presentation/forms/MonthGrid.vue` | internal/reexport | family composition |
| `src/presentation/forms/TimeColumns.vue` | internal/reexport | family composition |
| `src/presentation/forms/addressEditor/AddressEditor.vue` | yes | yes |
| `src/presentation/forms/calendarPicker/CalendarPicker.vue` | yes | yes |
| `src/presentation/forms/chatComposerInput/ChatComposerInput.vue` | yes | yes |
| `src/presentation/forms/checkboxField/CheckboxField.vue` | yes | yes |
| `src/presentation/forms/checkboxGroup/CheckboxGroup.vue` | yes | yes |
| `src/presentation/forms/checkboxInput/CheckboxInput.vue` | yes | yes |
| `src/presentation/forms/choiceCard/ChoiceCard.vue` | yes | yes |
| `src/presentation/forms/codeEditor/CodeEditor.vue` | yes | yes |
| `src/presentation/forms/colorArea/ColorArea.vue` | yes | yes |
| `src/presentation/forms/colorInput/ColorInput.vue` | yes | yes |
| `src/presentation/forms/colorPicker/ColorPicker.vue` | yes | yes |
| `src/presentation/forms/colorSliderInput/ColorSliderInput.vue` | yes | yes |
| `src/presentation/forms/colorSwatchPicker/ColorSwatchItem.vue` | internal/reexport | family composition |
| `src/presentation/forms/colorSwatchPicker/ColorSwatchPicker.vue` | yes | yes |
| `src/presentation/forms/colorWheelInput/ColorWheelInput.vue` | yes | yes |
| `src/presentation/forms/comboboxPicker/ComboboxPicker.vue` | yes | yes |
| `src/presentation/forms/comboboxPicker/ComboboxPickerContent.vue` | yes | yes |
| `src/presentation/forms/comboboxPicker/ComboboxPickerEmpty.vue` | yes | yes |
| `src/presentation/forms/comboboxPicker/ComboboxPickerGroup.vue` | yes | yes |
| `src/presentation/forms/comboboxPicker/ComboboxPickerInput.vue` | yes | yes |
| `src/presentation/forms/comboboxPicker/ComboboxPickerItem.vue` | yes | yes |
| `src/presentation/forms/comboboxPicker/ComboboxPickerSeparator.vue` | yes | yes |
| `src/presentation/forms/controlGroupField/ControlGroupField.vue` | yes | yes |
| `src/presentation/forms/cronInput/CronInput.vue` | yes | yes |
| `src/presentation/forms/currencyInput/CurrencyInput.vue` | yes | yes |
| `src/presentation/forms/dataGridEditor/CellEditor.vue` | internal/reexport | family composition |
| `src/presentation/forms/dataGridEditor/DataGridEditor.vue` | yes | yes |
| `src/presentation/forms/dateInput/DateInput.vue` | yes | yes |
| `src/presentation/forms/datePicker/DatePicker.vue` | yes | yes |
| `src/presentation/forms/dateRangePicker/DateRangePicker.vue` | yes | yes |
| `src/presentation/forms/dateTimeInput/DateTimeInput.vue` | yes | yes |
| `src/presentation/forms/editableInput/EditableInput.vue` | yes | yes |
| `src/presentation/forms/editableInput/EditableInputCancel.vue` | yes | yes |
| `src/presentation/forms/editableInput/EditableInputInput.vue` | yes | yes |
| `src/presentation/forms/editableInput/EditableInputPreview.vue` | yes | yes |
| `src/presentation/forms/editableInput/EditableInputSubmit.vue` | yes | yes |
| `src/presentation/forms/emailInput/EmailInput.vue` | yes | yes |
| `src/presentation/forms/emojiPicker/CategoryNav.vue` | internal/reexport | family composition |
| `src/presentation/forms/emojiPicker/EmojiGrid.vue` | internal/reexport | family composition |
| `src/presentation/forms/emojiPicker/EmojiPicker.vue` | yes | yes |
| `src/presentation/forms/emojiPicker/EmojiPickerPopover.vue` | yes | yes |
| `src/presentation/forms/emojiPicker/EmojiTile.vue` | internal/reexport | family composition |
| `src/presentation/forms/emojiSizePicker/EmojiSizePicker.vue` | yes | yes |
| `src/presentation/forms/field/Field.vue` | yes | yes |
| `src/presentation/forms/filePicker/FilePicker.vue` | yes | yes |
| `src/presentation/forms/fileUploadPicker/FileUploadPicker.vue` | yes | yes |
| `src/presentation/forms/fontPicker/FontPicker.vue` | yes | yes |
| `src/presentation/forms/gradientPicker/GradientPicker.vue` | yes | yes |
| `src/presentation/forms/iconPicker/IconPicker.vue` | yes | yes |
| `src/presentation/forms/jsonEditor/JsonEditor.vue` | yes | yes |
| `src/presentation/forms/jsonEditor/JsonEditorTextView.vue` | internal/reexport | family composition |
| `src/presentation/forms/jsonEditor/JsonEditorTreeNode.vue` | internal/reexport | family composition |
| `src/presentation/forms/jsonEditor/JsonEditorTreeView.vue` | internal/reexport | family composition |
| `src/presentation/forms/keyboardShortcutPicker/KeyboardShortcutPicker.vue` | yes | yes |
| `src/presentation/forms/knobInput/KnobInput.vue` | yes | yes |
| `src/presentation/forms/labeledField/LabeledField.vue` | yes | yes |
| `src/presentation/forms/listboxPicker/ListboxPicker.vue` | yes | yes |
| `src/presentation/forms/listboxPicker/ListboxPickerEmpty.vue` | yes | yes |
| `src/presentation/forms/listboxPicker/ListboxPickerGroup.vue` | yes | yes |
| `src/presentation/forms/listboxPicker/ListboxPickerItem.vue` | yes | yes |
| `src/presentation/forms/listboxPicker/ListboxPickerSeparator.vue` | yes | yes |
| `src/presentation/forms/markdownEditor/MarkdownEditor.vue` | yes | yes |
| `src/presentation/forms/maskedInput/MaskedInput.vue` | yes | yes |
| `src/presentation/forms/multiSelectPicker/MultiSelectPicker.vue` | yes | yes |
| `src/presentation/forms/multiSelectPicker/MultiSelectPickerContent.vue` | yes | yes |
| `src/presentation/forms/multiSelectPicker/MultiSelectPickerItem.vue` | yes | yes |
| `src/presentation/forms/multiSelectPicker/MultiSelectPickerTags.vue` | yes | yes |
| `src/presentation/forms/multiSelectPicker/MultiSelectPickerTrigger.vue` | yes | yes |
| `src/presentation/forms/nodeEditor/NodeEditor.vue` | yes | yes |
| `src/presentation/forms/numberInput/NumberInput.vue` | yes | yes |
| `src/presentation/forms/optionTileGroupField/OptionTileGroupField.vue` | yes | yes |
| `src/presentation/forms/optionTilePicker/OptionTilePicker.vue` | yes | yes |
| `src/presentation/forms/passwordInput/PasswordInput.vue` | yes | yes |
| `src/presentation/forms/percentInput/PercentInput.vue` | yes | yes |
| `src/presentation/forms/phoneInput/PhoneInput.vue` | yes | yes |
| `src/presentation/forms/pinInput/PinInput.vue` | yes | yes |
| `src/presentation/forms/radioField/RadioField.vue` | yes | yes |
| `src/presentation/forms/radioGroup/RadioGroup.vue` | yes | yes |
| `src/presentation/forms/radioInput/RadioInput.vue` | yes | yes |
| `src/presentation/forms/rangeCalendarPicker/RangeCalendarPicker.vue` | yes | yes |
| `src/presentation/forms/reactionPicker/ReactionPicker.vue` | yes | yes |
| `src/presentation/forms/recurrenceEditor/RecurrenceEditor.vue` | yes | yes |
| `src/presentation/forms/searchInput/SearchInput.vue` | yes | yes |
| `src/presentation/forms/segmentedPicker/SegmentedPicker.vue` | yes | yes |
| `src/presentation/forms/selectPicker/SelectPicker.vue` | yes | yes |
| `src/presentation/forms/selectPicker/SelectPickerContent.vue` | yes | yes |
| `src/presentation/forms/selectPicker/SelectPickerItem.vue` | yes | yes |
| `src/presentation/forms/selectPicker/SelectPickerTrigger.vue` | yes | yes |
| `src/presentation/forms/selectPicker/SelectPickerValue.vue` | yes | yes |
| `src/presentation/forms/sliderInput/SliderInput.vue` | yes | yes |
| `src/presentation/forms/sortableGroup/SortableGroup.vue` | yes | yes |
| `src/presentation/forms/sortableGroup/SortableGroupHandle.vue` | yes | yes |
| `src/presentation/forms/sortableGroup/SortableGroupItem.vue` | yes | yes |
| `src/presentation/forms/sortableGroup/SortableGroupMoveButton.vue` | yes | yes |
| `src/presentation/forms/switchField/SwitchField.vue` | yes | yes |
| `src/presentation/forms/switchInput/SwitchInput.vue` | yes | yes |
| `src/presentation/forms/tagsInput/TagsInput.vue` | yes | yes |
| `src/presentation/forms/telInput/TelInput.vue` | yes | yes |
| `src/presentation/forms/textAreaInput/TextAreaInput.vue` | yes | yes |
| `src/presentation/forms/textInput/TextInput.vue` | yes | yes |
| `src/presentation/forms/timeInput/TimeInput.vue` | yes | yes |
| `src/presentation/forms/timePicker/TimePicker.vue` | yes | yes |
| `src/presentation/forms/toggleGroup/ToggleGroup.vue` | yes | yes |
| `src/presentation/forms/toggleInput/ToggleInput.vue` | yes | yes |
| `src/presentation/forms/urlInput/UrlInput.vue` | yes | yes |
| `src/presentation/forms/wizardForm/WizardForm.vue` | yes | yes |
| `src/presentation/forms/wizardForm/WizardFormFooter.vue` | yes | yes |
| `src/presentation/forms/wizardForm/WizardFormStep.vue` | yes | yes |
| `src/presentation/forms/wizardForm/WizardFormSteps.vue` | yes | yes |
| `src/presentation/layout/anchorLayout/AnchorLayout.vue` | yes | yes |
| `src/presentation/layout/appShell/AppShell.vue` | yes | yes |
| `src/presentation/layout/appShell/AppShellAside.vue` | yes | yes |
| `src/presentation/layout/appShell/AppShellContent.vue` | yes | yes |
| `src/presentation/layout/appShell/AppShellFooter.vue` | yes | yes |
| `src/presentation/layout/appShell/AppShellHeader.vue` | yes | yes |
| `src/presentation/layout/appShell/AppShellMain.vue` | yes | yes |
| `src/presentation/layout/appShell/AppShellSidebar.vue` | yes | yes |
| `src/presentation/layout/aspectRatioLayout/AspectRatioLayout.vue` | yes | yes |
| `src/presentation/layout/boxLayout/BoxLayout.vue` | yes | yes |
| `src/presentation/layout/centerLayout/CenterLayout.vue` | yes | yes |
| `src/presentation/layout/clusterLayout/ClusterLayout.vue` | yes | yes |
| `src/presentation/layout/containerLayout/ContainerLayout.vue` | yes | yes |
| `src/presentation/layout/dividerLayout/DividerLayout.vue` | yes | yes |
| `src/presentation/layout/fieldsetLayout/FieldsetLayout.vue` | yes | yes |
| `src/presentation/layout/flexLayout/FlexLayout.vue` | yes | yes |
| `src/presentation/layout/frameLayout/FrameLayout.vue` | yes | yes |
| `src/presentation/layout/grid/Grid.vue` | yes | yes |
| `src/presentation/layout/hStackLayout/HStackLayout.vue` | yes | yes |
| `src/presentation/layout/inlineLayout/InlineLayout.vue` | yes | yes |
| `src/presentation/layout/inputAddonLayout/InputAddonLayout.vue` | yes | yes |
| `src/presentation/layout/inputGroup/InputGroup.vue` | yes | yes |
| `src/presentation/layout/navbar/Navbar.vue` | yes | yes |
| `src/presentation/layout/pullToRefreshLayout/PullToRefreshLayout.vue` | yes | yes |
| `src/presentation/layout/resizablePanelsLayout/ResizablePanel.vue` | yes | yes |
| `src/presentation/layout/resizablePanelsLayout/ResizablePanelsLayout.vue` | yes | yes |
| `src/presentation/layout/resizablePanelsLayout/ResizableSeparator.vue` | yes | yes |
| `src/presentation/layout/scrollArea/ScrollArea.vue` | yes | yes |
| `src/presentation/layout/section/Section.vue` | yes | yes |
| `src/presentation/layout/separatorLayout/SeparatorLayout.vue` | yes | yes |
| `src/presentation/layout/spacerLayout/SpacerLayout.vue` | yes | yes |
| `src/presentation/layout/stackLayout/StackLayout.vue` | yes | yes |
| `src/presentation/layout/surfaceLayout/SurfaceLayout.vue` | yes | yes |
| `src/presentation/layout/swipeActionsLayout/SwipeActionsLayout.vue` | yes | yes |
| `src/presentation/layout/tiltLayout/TiltLayout.vue` | yes | yes |
| `src/presentation/layout/twoColumnLayout/TwoColumnLayout.vue` | yes | yes |
| `src/presentation/layout/vStackLayout/VStackLayout.vue` | yes | yes |
| `src/presentation/nav/breadcrumb/Breadcrumb.vue` | yes | yes |
| `src/presentation/nav/contextMenu/ContextMenu.vue` | yes | yes |
| `src/presentation/nav/contextMenu/ContextMenuContent.vue` | yes | yes |
| `src/presentation/nav/contextMenu/ContextMenuTrigger.vue` | yes | yes |
| `src/presentation/nav/dropdownMenu/DropdownMenu.vue` | yes | yes |
| `src/presentation/nav/dropdownMenu/DropdownMenuContent.vue` | yes | yes |
| `src/presentation/nav/dropdownMenu/DropdownMenuTrigger.vue` | yes | yes |
| `src/presentation/nav/linkItem/LinkItem.vue` | yes | yes |
| `src/presentation/nav/menu/Menu.vue` | yes | yes |
| `src/presentation/nav/menu/MenuGroup.vue` | yes | yes |
| `src/presentation/nav/menu/MenuItem.vue` | yes | yes |
| `src/presentation/nav/menu/MenuLabel.vue` | yes | yes |
| `src/presentation/nav/menu/MenuSeparator.vue` | yes | yes |
| `src/presentation/nav/menubar/Menubar.vue` | yes | yes |
| `src/presentation/nav/menubar/MenubarContent.vue` | yes | yes |
| `src/presentation/nav/menubar/MenubarMenu.vue` | yes | yes |
| `src/presentation/nav/menubar/MenubarTrigger.vue` | yes | yes |
| `src/presentation/nav/navItem/NavItem.vue` | yes | yes |
| `src/presentation/nav/navigationMenu/NavigationMenu.vue` | yes | yes |
| `src/presentation/nav/navigationMenu/NavigationMenuContent.vue` | yes | yes |
| `src/presentation/nav/navigationMenu/NavigationMenuItem.vue` | yes | yes |
| `src/presentation/nav/navigationMenu/NavigationMenuLink.vue` | yes | yes |
| `src/presentation/nav/navigationMenu/NavigationMenuList.vue` | yes | yes |
| `src/presentation/nav/navigationMenu/NavigationMenuTrigger.vue` | yes | yes |
| `src/presentation/nav/pagination/Pagination.vue` | yes | yes |
| `src/presentation/nav/scrollSpy/ScrollSpy.vue` | yes | yes |
| `src/presentation/nav/tableOfContents/TableOfContents.vue` | yes | yes |
| `src/presentation/overlays/OverlayBody.vue` | internal/reexport | family composition |
| `src/presentation/overlays/OverlayCloseButton.vue` | internal/reexport | family composition |
| `src/presentation/overlays/OverlayDescription.vue` | internal/reexport | family composition |
| `src/presentation/overlays/OverlayFooter.vue` | internal/reexport | family composition |
| `src/presentation/overlays/OverlayHeader.vue` | internal/reexport | family composition |
| `src/presentation/overlays/OverlayTitle.vue` | internal/reexport | family composition |
| `src/presentation/overlays/actionSheet/ActionSheet.vue` | yes | yes |
| `src/presentation/overlays/actionSheet/ActionSheetAction.vue` | yes | yes |
| `src/presentation/overlays/actionSheet/ActionSheetCancel.vue` | yes | yes |
| `src/presentation/overlays/alertModal/AlertModal.vue` | yes | yes |
| `src/presentation/overlays/alertModal/AlertModalAction.vue` | yes | yes |
| `src/presentation/overlays/alertModal/AlertModalCancel.vue` | yes | yes |
| `src/presentation/overlays/alertModal/AlertModalContent.vue` | yes | yes |
| `src/presentation/overlays/backdropOverlay/BackdropOverlay.vue` | yes | yes |
| `src/presentation/overlays/bottomSheet/BottomSheet.vue` | yes | yes |
| `src/presentation/overlays/commandPaletteModal/CommandPaletteModal.vue` | yes | yes |
| `src/presentation/overlays/commandPaletteModal/CommandPaletteModalContent.vue` | yes | yes |
| `src/presentation/overlays/commandPaletteModal/CommandPaletteModalEmpty.vue` | yes | yes |
| `src/presentation/overlays/commandPaletteModal/CommandPaletteModalGroup.vue` | yes | yes |
| `src/presentation/overlays/commandPaletteModal/CommandPaletteModalInput.vue` | yes | yes |
| `src/presentation/overlays/commandPaletteModal/CommandPaletteModalItem.vue` | yes | yes |
| `src/presentation/overlays/commandPaletteModal/CommandPaletteModalList.vue` | yes | yes |
| `src/presentation/overlays/commandPaletteModal/CommandPaletteModalSeparator.vue` | yes | yes |
| `src/presentation/overlays/drawer/Drawer.vue` | yes | yes |
| `src/presentation/overlays/drawer/DrawerContent.vue` | yes | yes |
| `src/presentation/overlays/drawer/DrawerTrigger.vue` | yes | yes |
| `src/presentation/overlays/hoverCard/HoverCard.vue` | yes | yes |
| `src/presentation/overlays/hoverCard/HoverCardArrow.vue` | yes | yes |
| `src/presentation/overlays/hoverCard/HoverCardContent.vue` | yes | yes |
| `src/presentation/overlays/hoverCard/HoverCardTrigger.vue` | yes | yes |
| `src/presentation/overlays/modal/Modal.vue` | yes | yes |
| `src/presentation/overlays/modal/ModalContent.vue` | yes | yes |
| `src/presentation/overlays/modal/ModalTrigger.vue` | yes | yes |
| `src/presentation/overlays/popover/Popover.vue` | yes | yes |
| `src/presentation/overlays/popover/PopoverArrow.vue` | yes | yes |
| `src/presentation/overlays/popover/PopoverContent.vue` | yes | yes |
| `src/presentation/overlays/popover/PopoverTrigger.vue` | yes | yes |
| `src/presentation/overlays/tooltip/Tooltip.vue` | yes | yes |
| `src/presentation/overlays/tourPopover/TourPopover.vue` | yes | yes |

## Follow-up: autosave ordering and lifecycle

Transferred scope: `src/foundation/storage/hooks/UseAutosave.ts` and `tests/unit/foundation/storage/Autosave.dom.test.ts` only.

- One sink invocation runs at a time. Edits during that write coalesce to the newest trailing value, and a completed older write cannot overwrite newer pending status or its timestamp.
- `flush()` makes pending work ready immediately but retains serialization. It returns void and does not await durability; disposal still cancels work queued behind an active sink.
- `cancel()` and `enabled=false` discard queued work and invalidate active completion state. An already-started sink is observed until settlement; no claim is made that its external write can be undone.
- Disposal disarms the scheduler before publishing idle status, starts no hidden final write, and ignores late state/error callbacks while observing rejection.
- Sinks may acknowledge through synchronous void, `Result<void, AppError>`, or a promise/thenable of either. A Result failure becomes error status. A thrown exception remains the original object in the exposed error ref and onError; it is not translated into an expected Result failure.
- Error-observer rejections are observed and reported diagnostically. A sink that requires an immutable mutable-draft payload snapshots it before its first await; autosave does not choose a domain cloning policy.

Verification: 13 targeted tests passed (`/private/tmp/vue-autosave-final-tests.log`), scoped lint passed without warnings (`/private/tmp/vue-autosave-final-lint.log`), and source/test typecheck passed at the earlier implementation checkpoint (`/private/tmp/vue-autosave-typecheck.log`). Cases include burst coalescing, serialized async overlap, stale success/failure, cancel and reenable, foreign thenables, disposal with queued work, rejected active cleanup, explicit Result failure and rejected async error observers.

No design question remains. The parent owns the final integrated rerun after this source hold.


## Final row 35 canonical Vue model acceptance

The presentation audit covered all 379 SFC sources, including inherited field wrappers, internal editors and named axes. The migration below records 95 affected component surfaces; 97 adjacent specs were refreshed from the actual props/emits while preserving their behavior and verification sections. The governing owner is `conventions/development/frontend/core/lla/constructs/vue/macros.md` (controlled props): one primary model and one update event; named axes keep their meaning.

- Primary editable/selected values now use `modelValue`, `defaultValue` where uncontrolled behavior exists, and `update:modelValue`. Removed `value`, `checked`, `isPressed`, `sizeRatio` aliases only when they named the same model. Checkbox/Radio/Switch and inherited fields use the same primary Boolean model; optional Boolean models retain explicit `undefined` defaults.
- Disclosure roots use `open/defaultOpen/update:open`; duplicate `isOpen` and `open-change` are gone. Controlled-only Menu and UndoBar use `open/update:open`. Secondary inputValue/editing/view/mode/date/currentStep/sidebarOpen axes and named page/zoom/index/sortBy/expanded/nodes/sizes axes have one canonical update event.
- SelectPicker now emits the key (or null) once, with no second option-shaped event for that selection. Callers resolve associated option data by key. ColorArea preserves saturation and HSV value as two numeric named models; only changed axes emit, and reset uses those same update paths.
- `MonthGrid` state callbacks became `update:viewMonth` and `update:focusedDate`; query callbacks and activation actions stay distinct. `TimeColumns` and `CellEditor` use primary `modelValue` internally. ResizablePanelsLayout uses `update:sizes` instead of an onSizesChange callback prop.
- Item identity props (`value` on selection items, ToggleInput, CheckboxField, RadioField and ChoiceCard), read-only progress/chart values, and pure visibility flags (`isOpen` on BackdropOverlay, AnchorLayout and LoadingOverlay) are preserved. They are not duplicate writable model axes. File selection `files-change`, DataGrid cell-edit `row-change`, Listbox active-descendant notifications and ScrollSpy observed-section notifications remain action/observation contracts rather than replacement-model events.
- Native text/numeric/date input fallthrough cannot override the canonical committed value through an undeclared `value` attribute; native Boolean controls similarly own `checked`. Native submission item values remain available.

### Exact per-component migration

| Component | Prop/callback migration | Event migration |
|---|---|---|
| [AccordionGroup](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/display/accordionGroup/AccordionGroup.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [ActionSheet](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/overlays/actionSheet/ActionSheet.vue) | `isOpen` → `open` | `open-change` → `update:open` |
| [AddressEditor](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/addressEditor/AddressEditor.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [AlertModal](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/overlays/alertModal/AlertModal.vue) | `isOpen` → `open` | `open-change` → `update:open` |
| [AppShell](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/layout/appShell/AppShell.vue) | `isSidebarOpen` → `sidebarOpen` | `sidebar-open-change` → `update:sidebarOpen` |
| [BottomSheet](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/overlays/bottomSheet/BottomSheet.vue) | `isOpen` → `open` | `open-change` → `update:open` |
| [CalendarPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/calendarPicker/CalendarPicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [Carousel](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/display/carousel/Carousel.vue) | Unchanged | `index-change` → `update:index` |
| [CellEditor](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/dataGridEditor/CellEditor.vue) | `value` → `modelValue` | `update:value` → `update:modelValue` |
| [ChatComposerInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/chatComposerInput/ChatComposerInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [CheckboxField](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/checkboxField/CheckboxField.vue) | `checked` → `modelValue`; `defaultChecked` → `defaultValue` | `value-change` → `update:modelValue` |
| [CheckboxGroup](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/checkboxGroup/CheckboxGroup.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [CheckboxInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/checkboxInput/CheckboxInput.vue) | `checked` → `modelValue`; `defaultChecked` → `defaultValue` | `value-change` → `update:modelValue` |
| [ChoiceCard](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/choiceCard/ChoiceCard.vue) | `checked` → `modelValue`; `defaultChecked` → `defaultValue` | `value-change` → `update:modelValue` |
| [CodeEditor](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/codeEditor/CodeEditor.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [CollapsibleGroup](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/display/collapsibleGroup/CollapsibleGroup.vue) | `isOpen` → `open` | `open-change` → `update:open` |
| [ColorArea](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/colorArea/ColorArea.vue) | Unchanged | `value-change` → `update:saturation + update:value` |
| [ColorInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/colorInput/ColorInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [ColorPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/colorPicker/ColorPicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [ColorSliderInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/colorSliderInput/ColorSliderInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [ColorSwatchPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/colorSwatchPicker/ColorSwatchPicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [ColorWheelInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/colorWheelInput/ColorWheelInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [ComboboxPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/comboboxPicker/ComboboxPicker.vue) | `value` → `modelValue`; `isOpen` → `open` | `value-change` → `update:modelValue`; `open-change` → `update:open`; `input-change` → `update:inputValue` |
| [CommandPaletteModal](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/overlays/commandPaletteModal/CommandPaletteModal.vue) | `isOpen` → `open` | `open-change` → `update:open`; `input-change` → `update:inputValue` |
| [CronInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/cronInput/CronInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [CurrencyInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/currencyInput/CurrencyInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [DataTable](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/display/dataTable/DataTable.vue) | Unchanged | `sort-change` → `update:sortBy` |
| [DateInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/dateInput/DateInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [DatePicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/datePicker/DatePicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [DateRangePicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/dateRangePicker/DateRangePicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [DateTimeInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/dateTimeInput/DateTimeInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [DisclosureButton](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/actions/disclosureButton/DisclosureButton.vue) | `isOpen` → `open` | `open-change` → `update:open` |
| [Drawer](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/overlays/drawer/Drawer.vue) | `isOpen` → `open` | `open-change` → `update:open` |
| [DropdownMenu](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/nav/dropdownMenu/DropdownMenu.vue) | `isOpen` → `open` | `open-change` → `update:open` |
| [EditableInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/editableInput/EditableInput.vue) | `value` → `modelValue`; `isEditing` → `editing` | `value-change` → `update:modelValue`; `editing-change` → `update:editing` |
| [EmailInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/emailInput/EmailInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [EmojiPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/emojiPicker/EmojiPicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [EmojiPickerPopover](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/emojiPicker/EmojiPickerPopover.vue) | `value` → `modelValue`; `isOpen` → `open` | `value-change` → `update:modelValue`; `open-change` → `update:open` |
| [EmojiSizePicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/emojiSizePicker/EmojiSizePicker.vue) | `sizeRatio` → `modelValue` | `value-change` → `update:modelValue` |
| [EventCalendarViewer](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/display/eventCalendarViewer/EventCalendarViewer.vue) | Unchanged | `view-change` → `update:view`; `date-change` → `update:date` |
| [FontPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/fontPicker/FontPicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [GradientPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/gradientPicker/GradientPicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [HoverCard](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/overlays/hoverCard/HoverCard.vue) | `isOpen` → `open` | `open-change` → `update:open` |
| [IconPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/iconPicker/IconPicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [JsonEditor](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/jsonEditor/JsonEditor.vue) | `value` → `modelValue` | `value-change` → `update:modelValue`; `mode-change` → `update:mode` |
| [KeyboardShortcutPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/keyboardShortcutPicker/KeyboardShortcutPicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [KnobInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/knobInput/KnobInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [ListboxPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/listboxPicker/ListboxPicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [MarkdownEditor](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/markdownEditor/MarkdownEditor.vue) | `value` → `modelValue` | `value-change` → `update:modelValue`; `view-change` → `update:view` |
| [MaskedInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/maskedInput/MaskedInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [Menu](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/nav/menu/Menu.vue) | `isOpen` → `open` | `close` → `update:open` |
| [Menubar](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/nav/menubar/Menubar.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [Modal](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/overlays/modal/Modal.vue) | `isOpen` → `open` | `open-change` → `update:open` |
| [MonthGrid](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/MonthGrid.vue) | `onViewMonthChange` → `onUpdate:viewMonth`; `onFocusedDateChange` → `onUpdate:focusedDate` | Canonical listener in prop/callback column |
| [MultiSelectPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/multiSelectPicker/MultiSelectPicker.vue) | `value` → `modelValue`; `isOpen` → `open` | `value-change` → `update:modelValue`; `open-change` → `update:open` |
| [NavigationMenu](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/nav/navigationMenu/NavigationMenu.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [NodeEditor](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/nodeEditor/NodeEditor.vue) | Unchanged | `nodes-change` → `update:nodes` |
| [NumberInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/numberInput/NumberInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [Pagination](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/nav/pagination/Pagination.vue) | Unchanged | `page-change` → `update:page` |
| [PasswordInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/passwordInput/PasswordInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [PdfViewer](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/display/pdfViewer/PdfViewer.vue) | Unchanged | `page-change` → `update:page`; `zoom-change` → `update:zoom` |
| [PercentInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/percentInput/PercentInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [PhoneInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/phoneInput/PhoneInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [PinInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/pinInput/PinInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [Popover](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/overlays/popover/Popover.vue) | `isOpen` → `open` | `open-change` → `update:open` |
| [RadioField](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/radioField/RadioField.vue) | `checked` → `modelValue`; `defaultChecked` → `defaultValue` | `value-change` → `update:modelValue` |
| [RadioGroup](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/radioGroup/RadioGroup.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [RadioInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/radioInput/RadioInput.vue) | `checked` → `modelValue`; `defaultChecked` → `defaultValue` | `value-change` → `update:modelValue` |
| [RangeCalendarPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/rangeCalendarPicker/RangeCalendarPicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [RecurrenceEditor](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/recurrenceEditor/RecurrenceEditor.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [ResizablePanelsLayout](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/layout/resizablePanelsLayout/ResizablePanelsLayout.vue) | `onSizesChange` → `onUpdate:sizes` | Canonical listener in prop/callback column |
| [SearchInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/searchInput/SearchInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [SegmentedPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/segmentedPicker/SegmentedPicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [SelectPicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/selectPicker/SelectPicker.vue) | `value` → `modelValue`; `isOpen` → `open` | `value-change` → `update:modelValue`; `open-change` → `update:open` |
| [SliderInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/sliderInput/SliderInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [SpeedDialGroup](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/actions/speedDialGroup/SpeedDialGroup.vue) | `isOpen` → `open` | `open-change` → `update:open` |
| [StepperGroup](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/display/stepperGroup/StepperGroup.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [SwitchField](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/switchField/SwitchField.vue) | `checked` → `modelValue`; `defaultChecked` → `defaultValue` | `value-change` → `update:modelValue` |
| [SwitchInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/switchInput/SwitchInput.vue) | `checked` → `modelValue`; `defaultChecked` → `defaultValue` | `value-change` → `update:modelValue` |
| [TabsGroup](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/display/tabsGroup/TabsGroup.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [TagsInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/tagsInput/TagsInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue`; `input-change` → `update:inputValue` |
| [TelInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/telInput/TelInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [TextAreaInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/textAreaInput/TextAreaInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [TextInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/textInput/TextInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [TimeColumns](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/TimeColumns.vue) | `value` → `modelValue`; `onTimeChange` → `onUpdate:modelValue` | Canonical listener in prop/callback column |
| [TimeInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/timeInput/TimeInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [TimePicker](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/timePicker/TimePicker.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [ToggleGroup](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/toggleGroup/ToggleGroup.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [ToggleInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/toggleInput/ToggleInput.vue) | `isPressed` → `modelValue`; `defaultPressed` → `defaultValue` | `pressed-change` → `update:modelValue` |
| [Tooltip](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/overlays/tooltip/Tooltip.vue) | `isOpen` → `open` | `open-change` → `update:open` |
| [TourPopover](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/overlays/tourPopover/TourPopover.vue) | `isOpen` → `open` | `open-change` → `update:open`; `step-change` → `update:currentStep` |
| [TreeViewer](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/display/treeViewer/TreeViewer.vue) | `selectedValue` → `modelValue`; `defaultSelectedValue` → `defaultValue` | `selection-change` → `update:modelValue`; `expanded-change` → `update:expanded` |
| [UndoBar](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/feedback/undoBar/UndoBar.vue) | `isOpen` → `open` | `open-change` → `update:open` |
| [UrlInput](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/urlInput/UrlInput.vue) | `value` → `modelValue` | `value-change` → `update:modelValue` |
| [WizardForm](/Users/max/Projects/10x-ws/workbench/career/engineering/wow-two/wow-two-ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.ui/engineering/codebase/wow-two-front-vue-beta-sdk/src/presentation/forms/wizardForm/WizardForm.vue) | Unchanged | `step-change` → `update:currentStep` |

### Validation and file naming

- Presentation DOM + SSR: **32 files / 1,105 tests passed**, including seven new canonical-model tests. `/private/tmp/canonical-tests-final.log`.
- New assertions cover all exported model surfaces, preserved selection-item keys, native value ownership, inherited Boolean defaults, controlled accordion requests without caller-state mutation, AlertModal forwarding, changed-axis/reset ColorArea events and SelectPicker key-only updates. Existing composite reset cases still cover CheckboxGroup/ToggleGroup ownership, focused PIN cells and focused TagsInput after extra tags disappear.
- Source and test typecheck passed (`/private/tmp/canonical-types-final.log`); playground typecheck passed (`/private/tmp/canonical-playground-final.log`); all **407 package SFCs compile** (`/private/tmp/canonical-sfc-final.log`). Scoped lint and format were checked separately; the app is excluded from repository ESLint by configuration and is covered by its Vue typecheck.
- Row 25 filenames: `forms/useNativeFormReset.ts` → `forms/UseNativeFormReset.ts`; `forms/emojiPicker/useEmojiPicker.ts` → `forms/emojiPicker/UseEmojiPicker.ts`. Exported function identifiers stay lower camel case. All owned import paths were updated. After a macOS case-only patch move removed the source, both helpers were restored from the exact last-successful-build sourcemap source before validation; the native reset retains owner-document focus matching, stable control identity, cancelled reset and reassociated-form guards.
- No new design choice remains in this model-naming lane. Browser scenarios retain the previously documented runtime verification status; DOM/SSR tests do not claim browser keyboard proof. Parent owns the final package/build/browser aggregate gates.
