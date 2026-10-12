# Release preparation

- Validate all six new Rocky images and real EO processing on Minikube.
- Migrate the four legacy workflow input contracts to the PLAN.md typed CWL
  conventions, including quoted CRS codes and published shared schemas.
- Resolve whether the GeoParquet output should index original acquisitions
  or computed water masks; the legacy implementation currently indexes inputs.
- Select the next release version and validate published immutable artifacts.
