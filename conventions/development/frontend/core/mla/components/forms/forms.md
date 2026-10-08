# Forms

*Last updated: 2026-10-01*

> Which control or field to reach for, and with what values — the application register over the SDK's `forms/` group.
> Use case — picking between two inputs that both work, or fixing the value one carries here.
> What a control is → [control](../../constructs/visual/control.md).
> What a field is → [field](../../constructs/visual/field.md).
> The group's other constructs — [display](../../constructs/visual/display.md) ·
> [feedback](../../constructs/visual/feedback.md) · [layout](../../constructs/visual/layout.md) ·
> [form](../../domains/forms/forms.md).

## Components

| Component | Construct | Reach for it when |
|---|---|---|
| [AddressEditor](addressEditor.md) | control | a form posts a whole postal address as one value |
| [CalendarPicker](calendarPicker.md) | control | a date is picked from a month grid held inline |
| [CharacterCountCallout](characterCountCallout.md) | feedback | a limited field shows how much room is left |
| [ChatComposerInput](chatComposerInput.md) | control | a message is typed and sent from one row |
| [CheckboxField](checkboxField.md) | field | a checkbox needs its label beside the box |
| [CheckboxGroup](checkboxGroup.md) | control | several boxes share one name and one selection |
| [CheckboxInput](checkboxInput.md) | control | a box holds a boolean and is labelled from elsewhere |
| [ChoiceCard](choiceCard.md) | field | an option reads as a card with a title and a description |
| [CodeEditor](codeEditor.md) | control | code is edited with line numbers and tab indenting |
| [ColorArea](colorArea.md) | control | saturation and value are dragged on a square |
| [ColorInput](colorInput.md) | control | a hex colour is typed, with a live swatch beside it |
| [ColorPicker](colorPicker.md) | control | a colour is picked from a full panel behind a trigger |
| [ColorSliderInput](colorSliderInput.md) | control | one colour channel is dragged along a track |
| [ColorSwatchPicker](colorSwatchPicker.md) | control | a colour is picked from a fixed palette |
| [ColorSwatchPreview](colorSwatchPreview.md) | display | a colour is previewed as a chip |
| [ColorWheelInput](colorWheelInput.md) | control | hue is dragged around a ring |
| [ComboboxPicker](comboboxPicker.md) | control | a list is filtered by typing and one row is chosen |
| [CronInput](cronInput.md) | control | a cron string is built with a readable preview |
| [CurrencyInput](currencyInput.md) | control | a number carries a leading currency symbol |
| [DateInput](dateInput.md) | control | a date is typed, with a calendar on the trailing button |
| [DatePicker](datePicker.md) | control | a date is picked from a popover behind a trigger |
| [DateRangePicker](dateRangePicker.md) | control | both ends of a range are picked in one popover |
| [DateTimeInput](dateTimeInput.md) | control | a date and a wall-clock time are typed in one input |
| [EditableInput](editableInput.md) | control | text is read in place and edited on click |
| [EmailInput](emailInput.md) | control | the value is an email address |
| [EmojiPicker](emojiPicker.md) | control | an emoji is picked from a searchable, categorised grid |
| [EmojiSizePicker](emojiSizePicker.md) | control | an emoji's display size is picked from previews |
| [Field](field.md) | field | any control needs a label, a helper or an error |
| [FieldErrorCallout](fieldErrorCallout.md) | feedback | an error line is placed without a [Field](field.md) |
| [FieldHelperText](fieldHelperText.md) | display | a hint line is placed without a [Field](field.md) |
| [FieldsetLayout](fieldsetLayout.md) | layout | several fields answer to one name |
| [FilePicker](filePicker.md) | control | files are chosen through a styled trigger |
| [FileUploadPicker](fileUploadPicker.md) | control | files are dropped on a zone and validated |
| [FontPicker](fontPicker.md) | control | a font family is picked, each row in its own face |
| [GradientPicker](gradientPicker.md) | control | a gradient's kind, angle and stops are edited |
| [IconPicker](iconPicker.md) | control | an icon is picked from a searchable grid |
| [InputAddonLayout](inputAddonLayout.md) | layout | a fixed, uneditable string frames one input |
| [InputGroup](inputGroup.md) | layout | adjacent controls read as one connected control |
| [JsonEditor](jsonEditor.md) | control | JSON is edited as a tree or as raw text |
| [KeyboardShortcutPicker](keyboardShortcutPicker.md) | control | a key chord is captured by pressing it |
| [KnobInput](knobInput.md) | control | a value is dialled by rotation |
| [LabelText](labelText.md) | display | a control stands without a [Field](field.md) around it |
| [LegendText](legendText.md) | display | a [FieldsetLayout](fieldsetLayout.md) needs the name of its group |
| [ListboxPicker](listboxPicker.md) | control | rows are selected in place, with type-to-select |
| [MarkdownEditor](markdownEditor.md) | control | markdown is written beside a live preview |
| [MaskedInput](maskedInput.md) | control | the value follows a fixed character mask |
| [MultiSelectPicker](multiSelectPicker.md) | control | several options are chosen from one panel |
| [NumberInput](numberInput.md) | control | a number is typed or stepped |
| [PasswordInput](passwordInput.md) | control | a password is typed, with an optional reveal |
| [PasswordStrengthCallout](passwordStrengthCallout.md) | feedback | a typed password's strength is reported back |
| [PercentInput](percentInput.md) | control | a number carries a trailing `%` |
| [PhoneInput](phoneInput.md) | control | a dialling country and a number make one E.164 value |
| [PinInput](pinInput.md) | control | a one-time code is typed across single-character cells |
| [RadioField](radioField.md) | field | a radio needs its label beside the dot |
| [RadioGroup](radioGroup.md) | control | a mutex set owns the selected value |
| [RadioInput](radioInput.md) | control | one dot of a mutex set is labelled from elsewhere |
| [RangeCalendarPicker](rangeCalendarPicker.md) | control | both ends of a range are picked on an inline grid |
| [ReactionPicker](reactionPicker.md) | control | a reaction is picked from a short emoji row |
| [RecurrenceEditor](recurrenceEditor.md) | control | an RRULE is built from a frequency and an interval |
| [SearchInput](searchInput.md) | control | the value is a query, with a leading icon and a clear |
| [SelectPicker](selectPicker.md) | control | one option is chosen from a closed list |
| [SliderInput](sliderInput.md) | control | a number is dragged along a track |
| [StepperGroup](stepperGroup.md) | display | it owns the active step and swaps the panel behind it |
| [SwitchField](switchField.md) | field | a toggle applies at once and needs its label |
| [SwitchInput](switchInput.md) | control | a toggle holds a boolean, labelled from elsewhere |
| [TagsInput](tagsInput.md) | control | free-form tags are typed and committed as chips |
| [TelInput](telInput.md) | control | the value is a telephone number |
| [TextAreaInput](textAreaInput.md) | control | the value is multi-line text |
| [TextInput](textInput.md) | control | the value is one line of text and no variant fits |
| [TimeInput](timeInput.md) | control | a time is typed, with a popover on the trailing button |
| [TimePicker](timePicker.md) | control | a time is picked from popover columns |
| [UrlInput](urlInput.md) | control | the value is a URL |
| [WizardForm](wizardForm.md) | form | one submit is split into steps taken in order |
