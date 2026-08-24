# Forms

*Last updated: 2026-08-20*

> Which control or field to reach for, and with what values — the application register over the SDK's `forms/` group.
> Purpose — seventy-four components ship here, most of them controls; this folder says which one a case wants.
> Use case — picking between two inputs that both work, or fixing the value one carries here.
> What a control is → [control](../../constructs/visual/control.md).
> What a field is → [field](../../constructs/visual/field.md).
> The group's other constructs — [display](../../constructs/visual/display.md) ·
> [feedback](../../constructs/visual/feedback.md) · [layout](../../constructs/visual/layout.md) ·
> [form](../../domains/forms/forms.md).

## Components

| Component | Construct | Reach for it when |
|---|---|---|
| [AddressForm](addressForm.md) | form | a form posts a whole postal address as one value |
| [Calendar](calendar.md) | control | a date is picked from a month grid held inline |
| [CharacterCount](characterCount.md) | feedback | a limited field shows how much room is left |
| [ChatComposer](chatComposer.md) | control | a message is typed and sent from one row |
| [Checkbox](checkbox.md) | control | a box holds a boolean and is labelled from elsewhere |
| [CheckboxField](checkboxField.md) | field | a checkbox needs its label beside the box |
| [CheckboxGroup](checkboxGroup.md) | control | several boxes share one name and one selection |
| [ChoiceCard](choiceCard.md) | field | an option reads as a card with a title and a description |
| [CodeEditor](codeEditor.md) | control | code is edited with line numbers and tab indenting |
| [ColorArea](colorArea.md) | control | saturation and value are dragged on a square |
| [ColorInput](colorInput.md) | control | a hex colour is typed, with a live swatch beside it |
| [ColorPicker](colorPicker.md) | control | a colour is picked from a full panel behind a trigger |
| [ColorSlider](colorSlider.md) | control | one colour channel is dragged along a track |
| [ColorSwatch](colorSwatch.md) | display | a colour is previewed as a chip |
| [ColorSwatchPicker](colorSwatchPicker.md) | control | a colour is picked from a fixed palette |
| [ColorWheel](colorWheel.md) | control | hue is dragged around a ring |
| [Combobox](combobox.md) | control | a list is filtered by typing and one row is chosen |
| [CronInput](cronInput.md) | control | a cron string is built with a readable preview |
| [CurrencyInput](currencyInput.md) | control | a number carries a leading currency symbol |
| [DateInput](dateInput.md) | control | a date is typed, with a calendar on the trailing button |
| [DatePicker](datePicker.md) | control | a date is picked from a popover behind a trigger |
| [DateRangePicker](dateRangePicker.md) | control | both ends of a range are picked in one popover |
| [DateTimeInput](dateTimeInput.md) | control | a date and a wall-clock time are typed in one input |
| [Editable](editable.md) | control | text is read in place and edited on click |
| [EmailInput](emailInput.md) | control | the value is an email address |
| [EmojiPicker](emojiPicker.md) | control | an emoji is picked from a searchable, categorised grid |
| [EmojiSizeControl](emojiSizeControl.md) | control | an emoji's display size is picked from previews |
| [Field](field.md) | field | any control needs a label, a helper or an error |
| [Fieldset](fieldset.md) | layout | several fields answer to one name |
| [FilePicker](filePicker.md) | control | files are chosen through a styled trigger |
| [FileUpload](fileUpload.md) | control | files are dropped on a zone and validated |
| [FontPicker](fontPicker.md) | control | a font family is picked, each row in its own face |
| [FormErrorMessage](formErrorMessage.md) | feedback | an error line is placed without a [Field](field.md) |
| [FormHelperText](formHelperText.md) | display | a hint line is placed without a [Field](field.md) |
| [GradientPicker](gradientPicker.md) | control | a gradient's kind, angle and stops are edited |
| [IconPicker](iconPicker.md) | control | an icon is picked from a searchable grid |
| [InputAddon](inputAddon.md) | layout | a fixed, uneditable string frames one input |
| [InputGroup](inputGroup.md) | layout | adjacent controls read as one connected control |
| [JsonEditor](jsonEditor.md) | control | JSON is edited as a tree or as raw text |
| [KeyboardShortcutPicker](keyboardShortcutPicker.md) | control | a key chord is captured by pressing it |
| [Knob](knob.md) | control | a value is dialled by rotation |
| [Label](label.md) | display | a control stands without a [Field](field.md) around it |
| [LabeledInput](labeledInput.md) | field | never — the deprecated ancestor of [Field](field.md) |
| [Legend](legend.md) | display | a [Fieldset](fieldset.md) needs the name of its group |
| [Listbox](listbox.md) | control | rows are selected in place, with type-to-select |
| [MarkdownEditor](markdownEditor.md) | control | markdown is written beside a live preview |
| [MaskedInput](maskedInput.md) | control | the value follows a fixed character mask |
| [MultiSelect](multiSelect.md) | control | several options are chosen from one panel |
| [NumberInput](numberInput.md) | control | a number is typed or stepped |
| [PasswordInput](passwordInput.md) | control | a password is typed, with an optional reveal |
| [PasswordStrength](passwordStrength.md) | feedback | a typed password's strength is reported back |
| [PercentInput](percentInput.md) | control | a number carries a trailing `%` |
| [PhoneInput](phoneInput.md) | control | a dialling country and a number make one E.164 value |
| [PinInput](pinInput.md) | control | a one-time code is typed across single-character cells |
| [Radio](radio.md) | control | one dot of a mutex set is labelled from elsewhere |
| [RadioField](radioField.md) | field | a radio needs its label beside the dot |
| [RadioGroup](radioGroup.md) | control | a mutex set owns the selected value |
| [RangeCalendar](rangeCalendar.md) | control | both ends of a range are picked on an inline grid |
| [ReactionPicker](reactionPicker.md) | control | a reaction is picked from a short emoji row |
| [RecurrenceEditor](recurrenceEditor.md) | control | an RRULE is built from a frequency and an interval |
| [SearchInput](searchInput.md) | control | the value is a query, with a leading icon and a clear |
| [Select](select.md) | control | one option is chosen from a closed list |
| [Slider](slider.md) | control | a number is dragged along a track |
| [Stepper](stepper.md) | control | it owns the active step and swaps the panel behind it |
| [Switch](switch.md) | control | a toggle holds a boolean, labelled from elsewhere |
| [SwitchField](switchField.md) | field | a toggle applies at once and needs its label |
| [TagsInput](tagsInput.md) | control | free-form tags are typed and committed as chips |
| [TelInput](telInput.md) | control | the value is a telephone number |
| [TextAreaInput](textAreaInput.md) | control | the value is multi-line text |
| [TextInput](textInput.md) | control | the value is one line of text and no variant fits |
| [TimeInput](timeInput.md) | control | a time is typed, with a popover on the trailing button |
| [TimePicker](timePicker.md) | control | a time is picked from popover columns |
| [UrlInput](urlInput.md) | control | the value is a URL |
| [Wizard](wizard.md) | form | one submit is split into steps taken in order |
