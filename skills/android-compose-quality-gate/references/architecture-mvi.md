# Architecture: MVI and code organisation

## Per screen
- **Contract** `mvi/<Name>Contract.kt`: one `@Immutable data class <Name>State` (everything the screen draws, no callbacks), one `sealed interface <Name>Intent` (everything the user/system can do), one `sealed interface <Name>Effect` (one-shots: navigation, toast, dialog, permission request).
- **ViewModel** extends a small base (`MviViewModel<State, Intent, Effect>`) with `onIntent(intent)` as the only way in, `setState { copy(...) }` as the pure reducer, `sendEffect(...)` for one-shots, and `currentState` for reads (never collect your own flow inside the ViewModel).
- **Screen** = stateless composable taking `state` and `onIntent`, rendering only from state, plus a lifecycle-aware effects collector. No business logic in composables; no UI state that duplicates `UiState` except purely visual ones (scroll, focus, animation).
- Navigation comes from an effect or the nav graph, never from a composable body.
- Layers: composable -> ViewModel -> repository/use-case -> data source. ViewModels never touch Views or Context UI state; repositories never know state/intent types.
- Name intents for what the user did (analytics reports intent names); mark ones that should not be reported as silent.
- A read-only screen still gets a contract (empty intent/effect) so it can grow without a rewrite. A dialog's visual-only flag may stay local; anything the ViewModel must know lives in state.
- Previews and screenshot tests render from a hand-built immutable state, which is why state stays a plain value.

## Layout of a screen
`ui/screens/<name>/`: `<Name>Screen.kt` (stateful entry + stateless `<Name>Content(state, onIntent)`), `components/` (one composable per file named after it), `mvi/`, `<Name>ViewModel.kt`.
Shared UI goes to a shared component package only when **two or more screens** use it or it is a design-system element.

## Do not over-split
No file for a one-off few-line composable; no wrapper-around-a-wrapper, base class or interface without a second user. Extract when reused, when it has its own state/preview value, or when the file is hard to read (a UI file over ~250 lines is a smell, not a hard limit).

## Previews
Every component file and every `<Name>Content` has `@Preview` at the bottom, wrapped in the app theme, fed by hand-built state (never a ViewModel, DI or network). Cover default, loading, empty, error, long text / font scale 1.3, RTL, dark. Define multi-preview annotations once (sizes, font scale, RTL) instead of repeating parameters.

## Theme
Colours only through `MaterialTheme.colorScheme.<role>`; roles Material lacks are extension properties on `ColorScheme`, not a parallel accessor. Likewise `typography` and `shapes`. No hex colours, font sizes or radii in screens. Units are plain `dp`/`sp` taken 1:1 from the design frame.

## Cleanliness
Delete what a change makes dead (imports, files, resources, strings, commented code). No stray scratch files in the repo. One package per feature. Search for an existing component before writing a new one.
