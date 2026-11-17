# Network, cache and offline

## Requests
1. **Off the main thread, owned by the ViewModel** (`viewModelScope`) or a repository on `Dispatchers.IO`; never from a composable body. Work that must outlive the screen goes to WorkManager.
2. **Never repeated by accident** (recomposition, rotation, theme/locale change, double tap): load from `init` or the first intent guarded by state; `LaunchedEffect` keys are stable values; keep the running `Job` and ignore a second submit; search/filter cancels the previous job and debounces (~300 ms); disable the action and show progress while it runs; guard navigation/submit taps with a single-click guard (~500 ms).
3. **Every outcome handled:** success, empty, 4xx, 5xx, timeout, no network, unknown host, parse error, cancellation. The repository maps them to a sealed error/`Result`; it never throws into the UI. Rethrow `CancellationException`.
4. **Log technical, show general.** Endpoint, status, exception go to the logger (and a non-fatal crash report if unexpected), no personal data. The user sees a short friendly string resource, never an exception message, status code or "null".
5. Timeouts on the HTTP client. Retry automatically only idempotent reads, a few times with backoff; everything else retries on the user's tap.

## Remote data and lists: cache first
1. Single source of truth: observe the local cache (Room/DataStore) as a `Flow`; the network only refreshes it.
2. States: cache has items -> show at once, refresh quietly; no cache + online -> shimmer in the content's shape; no cache + offline -> a calm waiting state (no endless spinner, no error dialog); failed without cache -> error with Retry; failed with cache -> keep items + snackbar.
3. Follow connectivity: on offline -> online (`distinctUntilChanged`) refresh once and merge by stable id (no duplicates, no jump to top, scroll position kept). Lazy lists use stable `key` and `contentType`.
4. Paging: one page request at a time, footer shows loading or Retry, stop at the end.

## Offline and blocking actions
1. While planning mark each feature: works offline / needs network to view / needs network to submit. Nothing silently does nothing offline.
2. Input followed by an API call: check connectivity on submit; if offline show a blocking dialog (Retry / Cancel) and **keep what the user typed**. Input survives rotation and process death (`SavedStateHandle`). Disable submit while sending.
3. Channel: toast/snackbar for brief info that needs no decision (one at a time; snackbar if it has an action); dialog/sheet when the user must decide or the action is blocked; inline for field validation and section empty/error states.
4. Think like QA: airplane mode mid-request, slow network, rotation while loading, back while loading, double tap, process killed and reopened, permission revoked. Each ends in a sensible state, never a crash, frozen spinner or lost input.
