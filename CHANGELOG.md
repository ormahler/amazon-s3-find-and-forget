# Change Log

## v0.11 (unreleased)

- [#170](https://github.com/awslabs/amazon-s3-find-and-forget/pull/170): JSON
  support

## v0.10

- [#193](https://github.com/awslabs/amazon-s3-find-and-forget/pull/193): Add
  support for datasets with Pandas indexes. Pandas indexes will be preserved if
  present.
- [#194](https://github.com/awslabs/amazon-s3-find-and-forget/pull/194): Remove
  debugging code from Fargate task
- [#195](https://github.com/awslabs/amazon-s3-find-and-forget/pull/195): Fix
  support for requester pays buckets
- [#196](https://github.com/awslabs/amazon-s3-find-and-forget/pull/196): Upgrade
  backend dependencies
- [#197](https://github.com/awslabs/amazon-s3-find-and-forget/pull/197): Fix
  duplicated query executions during Find Phase

## v0.9

- [#189](https://github.com/awslabs/amazon-s3-find-and-forget/pull/189): UI
  Updates
- [#191](https://github.com/awslabs/amazon-s3-find-and-forget/pull/191): Deploy
  VPC template by default

## v0.8

- [#185](https://github.com/awslabs/amazon-s3-find-and-forget/pull/185): Fix
  dead links to VPC info in docs
- [#186](https://github.com/awslabs/amazon-s3-find-and-forget/pull/186): Fix:
  Solves an issue where the forget phase container could crash when redacting
  numeric Match IDs from its logs
- [#187](https://github.com/awslabs/amazon-s3-find-and-forget/pull/187):
  Dependency version updates for react-scripts

## v0.7

- [#183](https://github.com/awslabs/amazon-s3-find-and-forget/pull/183):
  Dependency version updates for elliptic

## v0.6

- [#173](https://github.com/awslabs/amazon-s3-find-and-forget/pull/173): Show
  column types and hierarchy in the front-end during Data Mapper creation
- [#173](https://github.com/awslabs/amazon-s3-find-and-forget/pull/173): Add
  support for char, smallint, tinyint, double, float
- [#174](https://github.com/awslabs/amazon-s3-find-and-forget/pull/174): Add
  support for types nested in struct
- [#177](https://github.com/awslabs/amazon-s3-find-and-forget/pull/177):
  Reformat of Python source code (non-functional change)
- Dependency version updates for:
  - [#178](https://github.com/awslabs/amazon-s3-find-and-forget/pull/178),
    [#180](https://github.com/awslabs/amazon-s3-find-and-forget/pull/180) lodash
  - [#179](https://github.com/awslabs/amazon-s3-find-and-forget/pull/179)
    websocket-extensions

## v0.5

- [#172](https://github.com/awslabs/amazon-s3-find-and-forget/pull/172): Fix for
  an issue where Make may not install the required Lambda layer dependencies,
  resulting in unusable builds.

## v0.4

- [#171](https://github.com/awslabs/amazon-s3-find-and-forget/pull/171): Fix for
  a bug affecting the API for 5xx responses not returning the appropriate CORS
  headers

## v0.3

- [#164](https://github.com/awslabs/amazon-s3-find-and-forget/pull/164): Fix for
  a bug affecting v0.2 deployment via CloudFormation

## v0.2

- [#161](https://github.com/awslabs/amazon-s3-find-and-forget/pull/161): Fix for
  a bug affecting Parquet files with nullable values generating a
  `Table schema does not match schema used to create file` exception during the
  Forget phase

## v0.1

Initial Release
