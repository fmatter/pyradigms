# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
* if a filter is specified for a parameter, the value order in `filters` is used
* `decorate_x` and `decorate_y` functions

### Removed

### Changed
* don't print index name in csv output

### Fixed

## [0.0.5] -- 2022-07-26

### Changed
* new: `pyd = Pyradigms()`
* allows keeping different pyradigm objects w/ different parameters
* under the hood: always use multiindex
* `long` format generates IDs if necessary

### Added
* docs
* tests

### Removed
* `x_sort` and `y_sort`
* `compose_from_csv` and `compose_from_text`
* `decompose_from_csv` and `decompose_from_text`

## [0.0.4] - 2021-04-12

First proper release.

[Unreleased]: https://github.com/fmatter/pyradigms/compare/0.0.5...HEAD
[0.0.5]: https://github.com/fmatter/pyradigms/releases/tag/0.0.5
[0.0.4]: https://github.com/fmatter/pyradigms/releases/tag/v0.0.4
