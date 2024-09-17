class PromptGenerator:
    COMMIT_MSG_PROMPT_TEMPLATE = """                                                                                                                                      
Below is a diff of all staged changes, coming from the command `git diff --cached`:                                                                                                            
---BEGIN DIFF---                                                                                                                                                           
{diff}                                                                                                                                                                     
---END DIFF---                                                                                                                                                             
Please generate a concise, one-line commit message for these changes. Be as specific as possible, generic messages like 'improved x, refactored y' are not useful at all."                                                                                                     
"""

    @staticmethod
    def get_commit_message_prompt(diff: str) -> str:
        return PromptGenerator.COMMIT_MSG_PROMPT_TEMPLATE.format(
            diff=diff) + ' Output strictly json in the format `{"msg": "YOUR_GENERATED_COMMIT_MESSAGE"}`'
