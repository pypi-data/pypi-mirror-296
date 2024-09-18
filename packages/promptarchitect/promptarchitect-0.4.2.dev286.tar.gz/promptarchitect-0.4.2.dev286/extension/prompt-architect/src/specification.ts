import matter from 'gray-matter';
import * as vscode from 'vscode';

export interface PromptFile {
    prompt: string;
    metadata: { [key: string]: string };
    tests: TestSpecification[];
}

export interface TestSpecification {
    identifier: string;
    label: string;
    uri: vscode.Uri;
}

function discoverTestSpecifications(fileUri: vscode.Uri, fileData: matter.GrayMatterFile<string>): TestSpecification[] {
    const testSpecifications: TestSpecification[] = [];

    for (const testIdentifier in fileData.data.tests) {
        const testMetadata = fileData.data.tests[testIdentifier];
        const testUri = vscode.Uri.joinPath(fileUri, testIdentifier);

        testSpecifications.push({
            identifier: testUri.toString(),
            label: testIdentifier,
            uri: fileUri
        });
    }

    return testSpecifications;
}

export function parsePromptFile(fileUri: vscode.Uri, content: string): PromptFile | undefined {
    try {
        const fileData = matter(content);
        const testSpecifications = discoverTestSpecifications(fileUri, fileData);

        return {
            prompt: fileData.content,
            metadata: fileData.data,
            tests: testSpecifications
        };
    } catch (e) {
        console.warn(`Failed to parse prompt file ${fileUri}`, e);
        return undefined;
    }
}