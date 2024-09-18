import * as vscode from 'vscode';
import { PromptFile, TestSpecification } from './specification';

interface TestItemMetadata {
    testCase?: TestSpecification | undefined
    promptFile?: PromptFile | undefined
}

export const testItemMetadata: WeakMap<vscode.TestItem, TestItemMetadata> = new WeakMap();

export function getOrCreateItemTree(controller: vscode.TestController, workspaceFolder: vscode.WorkspaceFolder, uri: vscode.Uri): vscode.TestItem {
    // Make sure we work from the workspaceFolder path down. No use to include some deep 
    // tree that the user can't relate to.
    const relativePath = uri.path.replace(workspaceFolder.uri.path, '');
    const pathElements = relativePath.split('/');

    let rootNode: vscode.TestItem | undefined = undefined;
    let parentNode: vscode.TestItem | undefined = undefined;

    while (pathElements.length > 0) {
        const currentElement = pathElements.shift();

        if (!currentElement) {
            continue;
        }

        // Try to find or create a root node when we're at the root of the path.
        // Otherwise try to find or create child nodes until all path elements are consumed.
        if (parentNode === undefined) {
            const nodeUri = uri.with({ path: `${workspaceFolder.uri.path}/${currentElement}` });
            const existingNode: vscode.TestItem | undefined = controller.items.get(nodeUri.toString());

            if (!existingNode) {
                rootNode = controller.createTestItem(nodeUri.toString(), currentElement, nodeUri);
                parentNode = rootNode;
                controller.items.add(rootNode);

                testItemMetadata.set(rootNode, { testCase: undefined, promptFile: undefined });
            } else {
                rootNode = existingNode;
                parentNode = existingNode;
            }
        }
        else {
            const nodeUri = uri.with({ path: `${parentNode.uri!.path}/${currentElement}` });
            const existingChildNode: vscode.TestItem | undefined = parentNode.children.get(nodeUri.toString());

            if (!existingChildNode) {
                const childNode = controller.createTestItem(nodeUri.toString(), currentElement!, nodeUri);
                parentNode.children.add(childNode);

                parentNode = childNode;

                testItemMetadata.set(childNode, {});
            }
            else {
                parentNode = existingChildNode;
            }
        }
    }

    return parentNode!;
}

export function gatherTestCases(testItems: readonly vscode.TestItem[]) {
    const testCases: TestSpecification[] = [];
    const queue: vscode.TestItem[] = [];

    for (const testItem of testItems) {
        queue.push(testItem);
    }

    while (queue.length > 0) {
        const testItem = queue.shift();
        const metadata = testItemMetadata.get(testItem!);

        if (metadata?.testCase) {
            testCases.push(metadata.testCase);
        }

        if (testItem?.children) {
            for (const [id, childTestItem] of testItem.children) {
                queue.push(childTestItem);
            }
        }
    }

    return testCases;
}

export function gatherTestItemsWithTestCases(testItem: vscode.TestItem) {
    const queue = [];
    const collector: vscode.TestItem[] = [];

    queue.push(testItem);

    while (queue.length > 0) {
        const currentItem = queue.shift();
        const metadata = testItemMetadata.get(currentItem!);

        if (metadata?.testCase) {
            collector.push(currentItem!);
        }

        if (currentItem?.children) {
            for (const [id, childTestItem] of currentItem.children) {
                queue.push(childTestItem);
            }
        }
    }

    return collector;
}