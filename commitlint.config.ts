import type { UserConfig } from "@commitlint/types";
import { RuleConfigSeverity } from "@commitlint/types";

const jiraTicketRegex = /^\(AIE-\d+(?:, ?AIE-\d+)*\)$/;

const Configuration: UserConfig = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "scope-empty": [RuleConfigSeverity.Error, "never"],
    "scope-format": [RuleConfigSeverity.Error, "always"],
    "scope-max-length": [RuleConfigSeverity.Error, "always", 35],
  },
  parserPreset: {
    parserOpts: {
      headerPattern:
        /^(?<type>\w*)(?<scope>\([\w\d\s-,]+\)?((?=:\s)|(?=!:\s)))?(?<breaking>!)?(?<subject>:\s.*)?|^(?<merge>Merge \w+)$/,
      headerCorrespondence: [
        "type",
        "scope",
        "breaking",
        "dummy",
        "subject",
        "merge",
      ],
    },
  },
  plugins: [
    {
      rules: {
          'scope-format': (parsed) => {
              const scope = parsed.scope;
              if (scope && !jiraTicketRegex.test(scope)) {
                  return [
                      false,
                      `scope must be a valid JIRA ticket`,
                  ];
              }
              return [true];
          },
      },
    },
  ],
};
export default Configuration;
