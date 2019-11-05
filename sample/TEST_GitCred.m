classdef (TestTags = {'git'}) TEST_GitCred < matlab.unittest.TestCase
    % GitCred
    %
    % Guidelines for Tester/Reviewer:
    % ---------------------------------------------------------------------
    %
    %  * Filename should be 'TEST_<UUT>' where <UUT> is the name of the
    %  unit under test (UUT). Each file should be scoped to a single
    %  unit/module.
    %
    %  * Test case name should clearly describes test's intent e.g.
    %  'test_normal_operation(testCase)' - the prefix of 'test_' is
    %  mandatory.
    %
    %  * Tests should be highly readable (it is the test procedure
    %  after all) and follow the below pattern:
    %
    %       1. Setup preconditions and data for the UUT.
    %
    %       2. Calls the UUT.
    %
    %       3. Assertions are used e.g. testCase.verifyEqual(...) with
    %       explicit valueExpected and valueActual declared where
    %       appropriate and any tolerances rationalised.
    %
    %       4. Do nothing else.
    %
    %  * Test cases are sensible and sufficient in that they excersise core
    %  functionality of UUT - ideally to 100% coverage.
    %
    %  * Where test input data is loaded ensure that the data is well
    %  described and its configuration (e.g. flight trials) or steps to
    %  reproduce are documented.
    %
    %  * Ensure test documentation (comments) are relevant and up to date.
    %
    %  * There should be instructions configured (externally) that describe
    %  how to run tests so that reviewers can execute and debug.
    %
    % Further Considerations:
    % ---------------------------------------------------------------------
    %  * Keep tests simple.
    %
    %  * Tests should be fast where possible - long tests can add to the
    %  technical debt: reduces the time of response and is an
    %  infrastructural burden.
    %
    %  * Consider creating an external helper class that abstracts and
    %  encapsulates information about environemnt and setup across
    %  multiple test files to reduce coupling e.g. folder structure or data
    %  folder name.
    %
    %  * Use test tags to group execution of tests results =
    %  runtests({'ExampleTagTest','ExampleTagClassTest'},'Tag','FeatureA');
    %
    %        classdef (TestTags = {'ers'}) TEST_algo < matlab.unittest.TestCase
    %
    %    Tags can also be applied at method/testcase level
    %
    % Unit Test Template: 
    % ---------------------------------------------------------------------
    % TBD instructions on where to get latest.
    
    properties
        % This contains all test properties that are accessible in any
        % non-static method (test case) using testCase.<property name>.
        
        cloneRoot % root directory for GIT cloning
        repoUrl = 'http://desuk27was045v:7990/scm/aws/configurator.git';
    end
    
    methods (TestClassSetup)
        % This is a test fixture that executes on startup once.
        %
        % Note that there is also a TestMethodSetup fixture that will run
        % before each individual test case.
        function setup(testCase)
            % perform class setup operations
            [~,fileName,~] = fileparts(tempname);
            testCase.cloneRoot = fullfile(pwd,fileName);
        end
    end
    
    methods (TestClassTeardown)
        % This is a test fixture that executes after all test cases have
        % been executed. it can be used to ensure environment is returned
        % to its original state e.g. deletes artefacts created during
        % testing.
        function teardown(testCase)
            % perform teardown operations.
        end
    end
    
    methods (TestMethodTeardown)
        % This test fixture will run after execution of each test case.
        function delete_clone_dir(testCase)
            % delete clone directories where approriate.
            if isfolder(testCase.cloneRoot)
                rmdir(testCase.cloneRoot,'s');
            end
        end
    end
    
    methods (Test)
        % This methods group contains all tests.
        
        function test_clone(testCase)
            % Test Objective:
            % -------------------------------------------------------------
            % The objective of this test is to test the cloning operation
            % but with git credentials.
            %
            % Pass Criteria:
            % -------------------------------------------------------------
            % The clone is succesful and the folder exists but was not
            % there prior to running UUT.
            
            % Test Input Data:
            % ----------------
            repo = testCase.repoUrl;
            branch = 'develop';
            cloneDir = fullfile(testCase.cloneRoot,'TEST_clone_w_cred');
            doesCloneDirExistPrior = isfolder(cloneDir);
            
            % Execute Unit Under Test:
            % ------------------------
            GC = GitCred();
            GC.clone(repo,branch,cloneDir);
            
            % Verification:
            % -------------
            testCase.verifyFalse(doesCloneDirExistPrior,'Cannot confirm test success as the folder existed prior.')
            
            doesCloneDirExistPost = isfolder(cloneDir);
            testCase.verifyTrue(doesCloneDirExistPost,'Failed to clone.')            
        end
        
        function test_clone_w_bad_repo_url(testCase)
            % Test Objective:
            % -------------------------------------------------------------
            % Attempts to clone a repository with a corrupted input repo
            % url
            %
            % Pass Criteria:
            % -------------------------------------------------------------
            % The clone directory was not created nor was it there prior.
            
            % Test Input Data:
            % ----------------
            repo = [testCase.repoUrl,'corruption'];
            branch = 'develop';
            cloneDir = fullfile(testCase.cloneRoot,'TEST_clone_w_cred');
            doesCloneDirExistPrior = isfolder(cloneDir);
            
            % Execute Unit Under Test:
            % ------------------------
            GC = GitCred();
            GC.clone(repo,branch,cloneDir);
            
            % Verification:
            % -------------
            testCase.verifyFalse(doesCloneDirExistPrior,'Cannot confirm test success as the folder existed prior.')
            
            doesCloneDirExistPost = isfolder(cloneDir);
            testCase.verifyFalse(doesCloneDirExistPost,'Folder is present when not expected.')            
        end
        
        function test_clone_master_branch(testCase)
            % Test Objective:
            % -------------------------------------------------------------
            % Attempts to clone a repository from the master branch.
            %
            % Pass Criteria:
            % -------------------------------------------------------------
            % The clone directory was created and there was not one prior.
            
            % Test Input Data:
            % ----------------
            repo = testCase.repoUrl;
            branch = 'master';
            cloneDir = fullfile(testCase.cloneRoot,'TEST_clone_w_cred');
            doesCloneDirExistPrior = isfolder(cloneDir);
            
            % Execute Unit Under Test:
            % ------------------------
            GC = GitCred();
            GC.clone(repo,branch,cloneDir);
            
            % Verification:
            % -------------
            testCase.verifyFalse(doesCloneDirExistPrior,'Cannot confirm test success as the folder existed prior.')
            
            doesCloneDirExistPost = isfolder(cloneDir);
            testCase.verifyTrue(doesCloneDirExistPost,'Failed to clone.')            
        end
        
        function test_clone_w_bad_branch(testCase)
            % Test Objective:
            % -------------------------------------------------------------
            % Attempts to clone a repository with a corrupted branch name.
            %
            % Pass Criteria:
            % -------------------------------------------------------------
            % The clone directory was not created nor was there one prior.
            
            % Test Input Data:
            % ----------------
            repo = testCase.repoUrl;
            branch = 'develop-corrupted';
            cloneDir = fullfile(testCase.cloneRoot,'TEST_clone_w_cred');
            doesCloneDirExistPrior = isfolder(cloneDir);
            
            % Execute Unit Under Test:
            % ------------------------
            GC = GitCred();
            GC.clone(repo,branch,cloneDir);
            
            % Verification:
            % -------------
            testCase.verifyFalse(doesCloneDirExistPrior,'Cannot confirm test success as the folder existed prior.')
            
            doesCloneDirExistPost = isfolder(cloneDir);
            testCase.verifyFalse(doesCloneDirExistPost,'Folder is present when not expected')            
        end
    end
    
    methods
        % This is a general method group which can be used to define methods
        % that are used by test cases.
    end
    
end