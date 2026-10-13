# Project Guide: claims-eligibility modernization

This is a simulated Blitzy-style modernization report for branch `blitzy/modernize-eligibility`. Blitzy did not produce it. The sections below follow that report shape: what changed, which files were touched, which tests were added, and what an engineer still has to do before production.

## Change summary

Service code `99441` (telehealth visit) was added to the in-memory coverage sets for `PPO-100` and `HMO-200`. Enrollment records, request validation, and reason strings were not modified. Eligibility still requires a known member, a plan code that matches that member's enrollment, and a service code present on the plan.

When those checks pass, the existing reason format is used:

- `Service 99441 is covered by plan PPO-100`
- `Service 99441 is covered by plan HMO-200`

A telehealth request remains ineligible when the member is unknown or the submitted plan does not match enrollment. Those responses keep the existing reason strings (`Member not found`, and `Member is enrolled in {enrolled_plan}, not {plan_code}`).

## Files touched

| File | Change |
| --- | --- |
| `app/main.py` | Added `99441` to `PLAN_COVERAGE` for `PPO-100` and `HMO-200`. |
| `tests/test_eligibility.py` | Added eligible and ineligible tests for service code `99441`. |
| `docs/PROJECT_GUIDE.md` | Added this modernization report. |

No other files were changed.

## Tests added

| Test | Expected result |
| --- | --- |
| `test_eligible_telehealth_on_ppo` | Member `M1001` on `PPO-100` is eligible for `99441`. |
| `test_eligible_telehealth_on_hmo` | Member `M1002` on `HMO-200` is eligible for `99441`. |
| `test_ineligible_telehealth_when_member_is_unknown` | Unknown member `M9999` requesting `99441` is ineligible. |
| `test_ineligible_telehealth_when_plan_does_not_match_enrollment` | Member `M1001` submitting `HMO-200` for `99441` is ineligible. |

Run the suite from the repository root after installing `requirements.txt`:

```bash
pytest
```

## Steps required before production

An engineer must complete each gate below. This report does not perform them.

1. **Review.** Inspect the coverage diff and the four new tests. Confirm `99441` belongs on both plans and that reason strings still match the existing format.
2. **Security scan.** Scan the branch for dependency and container findings before the image is promoted. This change does not alter authentication, dependencies, or the Dockerfile.
3. **Approval.** Obtain the required reviewer approval on `blitzy/modernize-eligibility` before merge.
4. **Deploy.** Merge the approved branch and deploy `claims-eligibility` through the existing release path. Do not treat this report as a production release.
