# Map Asset Versioning Process

This document outlines how to version, update, and roll back 2D and 3D map assets. It establishes naming conventions and describes how environment-specific branches are used to manage asset lifecycles.

## Naming Conventions

* **Asset files** use semantic versioning: `map_<name>_<type>_v<major>.<minor>.<patch>`.
  * `<name>` is a short identifier for the map.
  * `<type>` is `2d` or `3d`.
  * Example: `map_city_2d_v1.0.0`, `map_mall_3d_v2.1.0`.
* **Branches** follow the pattern `maps/<environment>`.
  * Standard environments: `dev`, `staging`, `prod`.
  * Example: `maps/dev`, `maps/staging`, `maps/prod`.

## Versioning Workflow

1. **Create** or update assets on the `maps/dev` branch.
2. **Commit** changes with descriptive messages referencing the asset name and version.
3. **Tag** stable releases with the asset version (e.g., `v1.0.0`).
4. **Merge** tested assets upward:
   * `maps/dev` → `maps/staging`
   * `maps/staging` → `maps/prod`

## Update Process

1. Checkout `maps/dev` and pull latest changes.
2. Add or modify asset files following the naming conventions.
3. Commit the changes and push to `maps/dev`.
4. Validate the assets in the development environment.
5. When ready, merge into `maps/staging` for further testing.
6. After acceptance, merge into `maps/prod` and tag the release.

## Rollback Strategy

* Use `git revert` on the relevant branch to undo a problematic commit.
* Alternatively, checkout a previous tag and merge it into the environment branch.
* For emergency production fixes, revert on `maps/prod` and backport the changes to `maps/staging` and `maps/dev`.

## Environment Branch Guidelines

* Keep environment branches long-lived and protected.
* Only merge upward (dev → staging → prod) to maintain stability.
* Avoid direct commits on `maps/prod`; use merges from `maps/staging`.

