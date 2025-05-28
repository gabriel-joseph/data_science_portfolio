Distinguish unintentional and intentional bias using examples.
Describe the sources of bias.

Bias is a common problem in data science and analysis. Simply put, bias means a finding or conclusion is statistically wronged due to flawed judgement or decision-making by the scientist. Despite widespread knowledge, bias remains a persistent problem in data science, but where does it come from? What are its origins and how do we fight against it?

First, we must compre unintentional vs intentional bias. The difference lies in the motive. Imagine two data scientists work for a politicial campaign and are tasked withed analyzing voter data. Analyst A believes in the political candidate on an ideological level, and they've convinced themselves that everyone will love the candidate. Analyst B is more down-to-earth and doesn't care about politics, but does their job with the bare minimum. When analyzing voter polls, Analyst A notices that the politician polls poorly with some demographics, but they shrug these polls off as outliers, flukes, noisey data, etc.

On the other hand, Analyst B doesn't care about politics and views the job as a paycheck. However, B is a bit lazy. When Analyst B does feature importance, they often run a shallow test and only analyze simple patterns rather than considering deeper, complex relationships. They opt for dropping incomplete or missing data rather than imputing missing values.

In this example, both analysts are biased in their work. Analyst A is ideologically driven, which influences their work. Because they are knowingly skewing the data, their bias is intentional. By comparison, Analyst B is simply "doing their job" and is not intending to skew the data. However their poor choice of actions (such as failing to clean data, scale data, test data) could also lower accuracy
