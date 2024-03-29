# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
* `update` function
* allow multiple values in cells
* `drop_empty` parameter

### Fixed
* z sorting
* drop empty cells from decomposed paradigm

## [0.1.0] -- 2022-10-30

### Changed
* duplicate values in a single paradigm cell are deleted

### Fixed
* docs generation
* complaints about missing values in sort order
* complaint about "unaccounted for" columns that are actually in `ignore`

## [0.0.6] -- 2022-09-28

### Added
* if a filter is specified for a parameter, the value order in `filters` is used
* `decorate`, `decorate_x` and `decorate_y` functions

### Changed
* don't print index name in csv output

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

[Unreleased]: https://github.com/fmatter/pyradigms/compare/0.1.0...HEAD
[0.1.0]: https://github.com/fmatter/pyradigms/releases/tag/0.1.0
[0.0.6]: https://github.com/fmatter/pyradigms/releases/tag/0.0.6
[0.0.5]: https://github.com/fmatter/pyradigms/releases/tag/0.0.5
[0.0.4]: https://github.com/fmatter/pyradigms/releases/tag/v0.0.4
