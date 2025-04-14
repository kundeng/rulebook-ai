# DEBUG (Debug MODE):
<WEB USE> Can use the web if needed using use_mcp_tool commands, particularly use the search tool from Perplexity. Example:
<use_mcp_tool>
    <server_name>perplexity-mcp</server_name>
    <tool_name>search</tool_name>
    <arguments>
        {
        "param1": "value1",
        "param2": "value2"
        }
    </arguments>
</use_mcp_tool>
</WEB USE>

<CLARIFICATION>
- Always ask for clarifications and follow-ups.
- Identify underspecified requirements and ask for detailed information.
- Fully understand all the aspects of the problem and gather details to make it very precise and clear.
- Ask towards all the hypothesis and assumptions needed to be made. Remove all the ambiguities and uncertainties.
- Suggest solutions that I didn't think about—anticipate my needs
- Only after having hundred percent clarity and confidence, proceed for SOLUTION.
</CLARIFICATION>

<DEBUG STEPS>
1. Reproduce the error
2. Understand the error
3. Find the error
4. Fix the error
5. Test the fix
</DEBUG STEPS>

<STUCK IN A LOOP>
1. Take a break
2. Try a different approach
3. Ask for help
4. Simplify the problem
5. Look for previously solved errors
</STUCK IN A LOOP>

<ERROR ANALYSIS>
1. Look at the error message
2. Look at the stack trace
3. Look at the code
4. Use a debugger
5. Use a logging statement
</ERROR ANALYSIS>

<LOOK FOR PREVIOUSLY SOLVED ERRORS>
1. Look at the error-documentation.mdc file
2. Look at the lessons-learned.mdc file
3. Look at the web
</LOOK FOR PREVIOUSLY SOLVED ERRORS>

# TESTING (Always write TEST after IMPLEMENTATION) [Code MODE]
<TESTING>

<DEPENDENCY BASED TESTING>
Create unit tests for any new functionality. Run all tests from the <ANALYZE CODE> to confirm that existing behavior is still as expected.
</DEPENDENCY BASED TESTING>
<NO BREAKAGE ASSERTION>
After you propose a change, run the tests yourself, and verify that it passes. Do not rely on me to do this, and be certain that my code will not be broken.
</NO BREAKAGE ASSERTION>

1. Write test logic in seperate files than the code implementation for teh functionality to keep the code clean and maintainable

<TEST PLAN>
- Think of sufficiently exhaustive test plans for the functionalities added/updated against the requirements and desired outcomes.
- Define comprehensive test scenarios covering edge cases
- Specify appropriate validation methods for the project's stack
- Suggest monitoring approaches to verify the solution's effectiveness
- Consider potential regressions and how to prevent them
</TEST PLAN>

2. Write test code for ANY added critical functionality ALWAYS. For initial test generation use <DEPENDENCY BASED TESTING> and <NO BREAKAGE ASSERTION>. Then use <TEST PLAN> to write code for extensive testing.
3. Document testing as specified in @memory.mdc
</TESTING>
