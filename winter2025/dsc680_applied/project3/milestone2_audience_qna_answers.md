# Milestone 2 Audience Q&A Answers

These responses are based on the Milestone 2 draft white paper, the pilot dataset (`n = 2400`), and the Milestone 2 notebook outputs. Where the final Kaggle-based model has not yet been run, the answer distinguishes between the current pilot result and the planned final-model step.

## 1. How were screen-time variables harmonized across datasets that define use differently?

Screen-use variables were mapped into a common schema measured in `hours/day`. The harmonized fields were:

- `screen_hours_total`
- `social_media_hours`
- `gaming_hours`
- `streaming_hours`
- `education_hours`

The goal was to make direction and units consistent before modeling. If a source reported only total screen exposure, it could still contribute to `screen_hours_total`. Subtype variables were only used when the source definition was specific enough to map cleanly. Outcome variables were also aligned to consistent scales, and the draft composite mental-health index was built from standardized anxiety and depression measures so that both components contributed comparably.

## 2. Why was 7.5 hours selected as the poor-sleep threshold, and how sensitive are results to that cutoff?

The `7.5`-hour cutoff was chosen as a practical milestone threshold: it is stricter than a general "adequate sleep" framing, but not so strict that the event becomes too rare to interpret for stakeholders. It also gave a clean binary target for the pilot logistic model.

In the pilot data:

- At `< 7.5` hours, poor-sleep prevalence was `4.9%`, and each additional screen hour was associated with `OR = 2.256` (`95% CI 1.808 to 2.815`).
- At `< 7.0` hours, the association remained positive at `OR = 2.164`, but the event rate dropped to `0.9%`.
- At `< 8.0` hours, the association remained positive at `OR = 1.914`, and the event rate increased to `14.0%`.

So the substantive conclusion did not change across reasonable thresholds: more screen time still corresponded to higher sleep-risk odds. The `7.5`-hour rule is a balance between interpretability and statistical stability.

## 3. Do associations differ by age group, sex, or socioeconomic status after adjustment?

In the pilot models, age-group and sex interactions were not strong after adjustment. The interaction terms between screen hours and age group were not statistically significant in either the OLS or logistic models, and the screen-hours-by-sex interaction was also not significant.

The main exception was socioeconomic status in the poor-sleep logistic model. The `screen_hours_total x ses_index` interaction reached significance (`p = 0.0406`), with a negative interaction coefficient. That suggests the adverse sleep-risk gradient was steeper for lower-SES youth and somewhat attenuated at higher SES levels.

Unadjusted descriptive patterns still matter:

- Average screen time rose by age group from about `2.99` hours (`10-12`) to `4.31` (`13-15`) to `5.52` (`16-18`).
- Poor-sleep prevalence also rose sharply across those age bands.

So the descriptive burden is clearly higher among older youth, even though the adjusted screen-time slope itself did not differ strongly by age or sex in the pilot run.

## 4. Which subtype of screen use has the largest adjusted effect?

That depends on the outcome:

- For the continuous mental-health index, the largest standardized OLS effects were essentially tied between `streaming_hours` (`beta = 0.298`) and `social_media_hours` (`beta = 0.297`), followed by `gaming_hours` (`beta = 0.275`) and `education_hours` (`beta = 0.213`).
- For poor-sleep risk, the largest adjusted logistic odds ratios were `gaming_hours` (`OR = 2.513`) and `streaming_hours` (`OR = 2.499`), then `social_media_hours` (`OR = 2.387`) and `education_hours` (`OR = 2.344`).

The important interpretation is that the subtype effects were all directionally adverse and fairly close to one another. The pilot does not support a simple claim that only one screen subtype matters.

## 5. How were missing values handled, and did alternative imputation strategies change results?

Milestone 2 used median imputation for low-rate missingness in:

- `screen_hours_total`
- `sleep_hours`
- `physical_activity_min`
- `anxiety_score`
- `depression_score`

That choice was deliberate because median imputation is simple, robust to skew, and appropriate for a draft-stage pilot pipeline.

The results were stable under alternative handling:

- OLS screen-time coefficient was `0.213` with median imputation, `0.212` with mean imputation, and `0.223` in complete-case analysis.
- Logistic poor-sleep odds ratio was `2.256` with median imputation, `2.259` with mean imputation, and `2.393` in complete-case analysis (`n = 2052`).

So the headline conclusion did not depend on one specific low-complexity imputation choice.

## 6. What diagnostics were used to check model assumptions and multicollinearity?

For multicollinearity, variance inflation factors were low:

- `screen_hours_total`: `2.530`
- `age`: `2.112`
- `ses_index`: `1.132`
- `sleep_hours`: `2.296`
- `physical_activity_min`: `1.534`

Those values are well below common concern thresholds, so multicollinearity does not appear to be a major issue in the pilot specification.

For OLS diagnostics, I checked heteroskedasticity, residual normality, and influence:

- Breusch-Pagan `p = 0.0026`, suggesting mild heteroskedasticity
- Jarque-Bera `p < 0.001`, suggesting residual non-normality
- Maximum Cook's distance was `0.0109`, indicating no single observation was dominating the fit

The practical takeaway is that the models are usable for Milestone 2, but the final version should report robust standard errors and include residual-vs-fitted and Q-Q diagnostics in the appendix.

## 7. How robust are findings if extreme high-use observations are excluded?

The results were not being driven by a few extreme users.

When I removed the top `1%` of `screen_hours_total` observations above about `7.73` hours/day:

- OLS coefficient changed from `0.213` to `0.212`
- Logistic poor-sleep odds ratio changed from `2.256` to `2.342`

When I applied a stricter filter and removed observations at `9+` hours/day:

- OLS coefficient stayed at `0.213`
- Logistic poor-sleep odds ratio was `2.247`

So the direction, magnitude, and significance of the core finding remained stable.

## 8. What additional confounders are planned for the final model?

The final model should add confounders if they are available consistently across the merged real-source datasets. The highest-value additions would be:

- family environment and parental monitoring
- baseline sleep disorders or baseline mental-health conditions
- school workload or homework burden
- bullying or social stress exposure
- household device rules and bedtime media access
- caffeine use or other sleep-disrupting behaviors
- chronic health conditions

If those variables are not consistently available across source datasets, they will be documented as residual confounding limits rather than forced into a weak harmonization.

## 9. How should schools apply these findings without overgeneralizing or stigmatizing students?

Schools should use the findings as a prevention and support signal, not as a punishment tool. The appropriate application is to identify patterns that merit supportive intervention, such as sleep education, counseling referrals, physical-activity promotion, and parent communication.

The findings should not be used to label individual students as "at risk" solely because of device use, and they should not justify blanket disciplinary device policies without context. The study is association-based, not causal, so the most responsible school response is targeted support and environmental improvement, not over-policing.

## 10. What action should the government take in addressing these findings?

The government should not treat one cross-sectional study as a reason for blunt legal screen-time limits. A better response is to combine public-health guidance, research support, and youth-protection policy.

The most defensible actions would be:

- fund longitudinal and causal research on youth screen use, sleep, and mental health
- expand population surveillance so screen exposure, sleep, and distress are measured consistently
- support school and community programs focused on sleep hygiene, mental-health access, and physical activity
- issue clearer parent-facing guidance that emphasizes context, bedtime routines, and subtype-specific risk
- strengthen youth-focused platform transparency and safety standards, especially around persuasive design and nighttime engagement

In short, the policy response should be evidence-based and preventive, not punitive.
