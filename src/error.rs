// Copyright 2022-2022 Tauri Programme within The Commons Conservancy
// SPDX-License-Identifier: Apache-2.0
// SPDX-License-Identifier: MIT

use thiserror::Error;

pub use crate::accelerator::AcceleratorParseError;

/// Errors returned by muda.
#[non_exhaustive]
#[derive(Error, Debug)]
pub enum Error {
    #[error("This menu item is not a child of this `Menu` or `Submenu`")]
    NotAChildOfThisMenu,
    #[cfg(windows)]
    #[error("This menu has not been initialized for this hwnd`")]
    NotInitialized,
    #[cfg(all(
        any(
            target_os = "linux",
            target_os = "dragonfly",
            target_os = "freebsd",
            target_os = "netbsd",
            target_os = "openbsd"
        ),
        feature = "gtk"
    ))]
    #[error("This menu has not been initialized for this gtk window`")]
    NotInitialized,
    #[cfg(windows)]
    #[error("This menu has already been initialized for this hwnd`")]
    AlreadyInitialized,
    #[cfg(all(
        any(
            target_os = "linux",
            target_os = "dragonfly",
            target_os = "freebsd",
            target_os = "netbsd",
            target_os = "openbsd"
        ),
        feature = "gtk"
    ))]
    #[error("This menu has already been initialized for this gtk window`")]
    AlreadyInitialized,
    #[error(transparent)]
    AcceleratorParseError(#[from] AcceleratorParseError),
    /// A menu bridge call failed on the OpenHarmony worker thread. Retained
    /// for API compatibility only — the OHOS backend no longer constructs
    /// this variant (bridge calls are fire-and-forget; a stale failure must
    /// not block or swallow the current call's dispatch). Bridge failures
    /// are exposed via `muda::last_bridge_error()` instead.
    #[cfg(target_env = "ohos")]
    #[error("OHOS menu bridge error: {0}")]
    OhosBridgeError(String),
}

/// Convenient type alias of Result type for muda.
pub type Result<T> = std::result::Result<T, Error>;
