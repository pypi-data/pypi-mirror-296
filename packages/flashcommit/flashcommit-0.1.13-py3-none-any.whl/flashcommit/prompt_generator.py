class PromptGenerator:
    COMMIT_MSG_PROMPT_TEMPLATE = """                                                                                                                                      
Below is a diff of all staged changes, coming from the command:                                                                                                            
---BEGIN DIFF---                                                                                                                                                           
{diff}                                                                                                                                                                     
---END DIFF---                                                                                                                                                             
Please generate a concise, one-line commit message for these changes. Be as specific as possible, generic messages like 'improved x, refactored y' are not useful at all."                                                                                                     
"""

    DIFF_PROMPT_TEMPLATE = """     
You are an expert Software Engineer and Code Reviewer.                                                                                                                                          
Review the following code diff and give actionable advice to improve the code. If possible show a proper solution as real code. Otherwise don't provide a patch.
Never give positiv comments or explain what as changed only proposed changes are welcome.                                         
---BEGIN DIFF---                                                                                                                                                           
{diff}                                                                                                                                                                     
---END DIFF---                                                                                                                                                           
"""

    EXAMPLE_PATCH = """
diff --git a/codex-client.py b/codex-client.py
index 25505ed..1a06bc9 100755
--- a/codex-client.py
+++ b/codex-client.py
@@ -222,5 +222,7 @@
     if __name__ == "__main__":
         print(client.do_parse(args.base, args.head))
     elif args.action == "REPO_INIT":
         print(client.do_repo_init(args.repository))
+    elif args.action == "FLASH_COMMIT":
+        print(client.do_repo_init(args.repository))
     else:
         raise Exception(f"No such action {args.action}")
"""

    @staticmethod
    def get_review_prompt(diff: str) -> str:
        xml_format = """
        <steps>
            <step>
                <file>FILENAME</file>
                <comment>YOUR_REASONING_ABOUT_THE_CHANGE</comment>
                <patch>UNIFIED_DIFF_OF_YOUR_SUGGESTED_CHANGE</patch>
            <step>
        </steps>
        """
        return PromptGenerator.DIFF_PROMPT_TEMPLATE.format(
            diff=diff) + (
            f'Provide your suggestions step by step in XML, strictly in the format `{xml_format.strip()}`. '
            f'Be sure to properly escape any "<" or ">" characters inside those tags!'
            f'UNIFIED_DIFF_OF_YOUR_SUGGESTED_CHANGE must be in the complete git patch format including a git patch header and correct hunk headers. '
            f'Never provide a patch for the changes you are reviewing, only patches for your improvments.'
            f'Especially pay attention to have the line numbers correct. '
            f'Always add at least two lines of context around each change. The patch must never end with a "+" or "-" line. '
            f'Here is an example of a correct patch: {PromptGenerator.EXAMPLE_PATCH}')

    @staticmethod
    def get_commit_message_prompt(diff: str) -> str:
        return PromptGenerator.COMMIT_MSG_PROMPT_TEMPLATE.format(
            diff=diff) + ' Output strictly json in the format `{"msg": "YOUR_GENERATED_COMMIT_MESSAGE"}`'
