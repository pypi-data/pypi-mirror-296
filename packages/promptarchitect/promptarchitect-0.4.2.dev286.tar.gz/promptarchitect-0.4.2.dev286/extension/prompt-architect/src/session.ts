import { exec } from 'child_process';
import * as vscode from 'vscode';
import { parsePromptFile } from './specification';
import { gatherTestCases, gatherTestItemsWithTestCases, getOrCreateItemTree, testItemMetadata } from './tree';

export class InteractiveTestSession {
    private controller: vscode.TestController;

    constructor(controller: vscode.TestController) {
        this.controller = controller;

        controller.resolveHandler = this.resolveHandler.bind(this);

        controller.createRunProfile(
            'Run tests',
            vscode.TestRunProfileKind.Run,
            this.runHandler.bind(this),
            true, undefined, false);
    }

    dispose() {
        this.controller.dispose();
    }

    private async runHandler(request: vscode.TestRunRequest) {
        if (!request.include) {
            this.runAllTests(request);
        } else {
            const runnableTests = gatherTestCases(request.include);
            console.log(runnableTests);
        }
    }

    private runAllTests(request: vscode.TestRunRequest) {
        const executablePath = this.resolvePromptArchitectExecutable();
        const testItems = this.gatherTestSpecificationsFromController();

        const run = this.controller.createTestRun(request, "Run all tests", true);

        for (const item of testItems) {
            run.started(item);
        }

        exec(executablePath, (error, stdout, stderr) => {
            if (error) {
                run.appendOutput(stderr);

                for (const item of testItems) {
                    run.errored(item, { message: error.message });
                }
            }
            else if (stderr) {
                run.appendOutput(stderr);

                this.controller.items.forEach(item => {
                    run.errored(item, { message: stderr });
                });
            }
            else {
                //TODO: Parse the output of the prompt architect tool and update the test items accordingly.
                run.appendOutput(stdout);
            }

            run.end();
        });
    }

    gatherTestSpecificationsFromController() {
        const testItems: vscode.TestItem[] = [];

        this.controller.items.forEach(item => {
            const childItems = gatherTestItemsWithTestCases(item);
            testItems.push(...childItems);
        });

        return testItems;
    }

    private resolvePromptArchitectExecutable(): string {
        const executablePath = vscode.workspace.getConfiguration("promptarchitect").get<string>("executablePath");
        return executablePath || 'promptarchitect';
    }

    private async resolveHandler(test: vscode.TestItem | undefined) {
        if (!test) {
            await this.resolveAllTestCases();
        } else {
            await this.parseTestFile(test);
        }
    }

    private async resolveAllTestCases() {
        if (!vscode.workspace.workspaceFolders) {
            return [];
        }

        return Promise.all(vscode.workspace.workspaceFolders.map(async (workspaceFolder) => {
            const pattern = new vscode.RelativePattern(workspaceFolder, "**/*.prompt");

            for (const x of await vscode.workspace.findFiles(pattern)) {
                const promptFileItem = getOrCreateItemTree(this.controller, workspaceFolder, x);
                this.parseTestFile(promptFileItem);
            }
        }));
    }

    private async parseTestFile(testFile: vscode.TestItem, contents?: string) {
        if (!contents) {
            const rawFileContent = await vscode.workspace.fs.readFile(testFile.uri!);
            contents = new TextDecoder().decode(rawFileContent);
        }

        const promptFile = parsePromptFile(testFile.uri!, contents);

        if (!testItemMetadata.has(testFile)) {
            testItemMetadata.set(testFile, {
                promptFile: promptFile
            });
        }

        if (!promptFile) {
            return;
        }

        for (const testSpecification of promptFile.tests) {
            const existingTestItem = testFile.children.get(testSpecification.identifier);

            if (!existingTestItem) {
                const testSpecificationItem = this.controller.createTestItem(
                    testSpecification.identifier,
                    testSpecification.label,
                    testSpecification.uri
                );

                testFile.children.add(testSpecificationItem);

                testItemMetadata.set(testSpecificationItem, {
                    testCase: testSpecification,
                });
            }
        }

        const removableItems: string[] = [];

        for (const [id, _] of testFile.children) {
            if (!promptFile.tests.some(test => test.identifier === id)) {
                removableItems.push(id);
            }
        }

        for (const id of removableItems) {
            testFile.children.delete(id);
        }
    }
}