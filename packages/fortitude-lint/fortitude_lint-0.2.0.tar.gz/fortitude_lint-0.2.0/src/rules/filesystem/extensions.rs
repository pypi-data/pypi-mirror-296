use crate::violation;
use crate::{Method, Rule, Violation};
use std::path::Path;
/// Defines rule that enforces use of standard file extensions.

fn non_standard_file_extension(path: &Path) -> Option<Violation> {
    let msg: &str = "file extension should be '.f90' or '.F90'";
    match path.extension() {
        Some(ext) => {
            // Must check like this as ext is an OsStr
            if ["f90", "F90"].iter().any(|&x| x == ext) {
                None
            } else {
                Some(violation!(msg))
            }
        }
        None => Some(violation!(msg)),
    }
}

pub struct NonStandardFileExtension {}

impl Rule for NonStandardFileExtension {
    fn method(&self) -> Method {
        Method::Path(non_standard_file_extension)
    }

    fn explain(&self) -> &str {
        "
        The standard file extensions for modern (free-form) Fortran are '.f90' or  '.F90'.
        Forms that reference later Fortran standards such as '.f08' or '.F95' may be rejected
        by some compilers and build tools.
        "
    }

    fn entrypoints(&self) -> Vec<&str> {
        vec!["PATH"]
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::violation;

    #[test]
    fn test_bad_file_extension() {
        let path = Path::new("my/dir/to/file.f95");
        assert_eq!(
            non_standard_file_extension(&path),
            Some(violation!["file extension should be '.f90' or '.F90'"]),
        );
    }

    #[test]
    fn test_missing_file_extension() {
        let path = Path::new("my/dir/to/file");
        assert_eq!(
            non_standard_file_extension(&path),
            Some(violation!["file extension should be '.f90' or '.F90'"]),
        );
    }

    #[test]
    fn test_correct_file_extensions() {
        let path1 = Path::new("my/dir/to/file.f90");
        let path2 = Path::new("my/dir/to/file.F90");
        assert_eq!(non_standard_file_extension(&path1), None);
        assert_eq!(non_standard_file_extension(&path2), None);
    }
}
