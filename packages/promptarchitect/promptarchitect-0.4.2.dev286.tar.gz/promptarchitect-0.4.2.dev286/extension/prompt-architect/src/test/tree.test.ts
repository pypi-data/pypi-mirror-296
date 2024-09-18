import * as assert from 'assert';
import * as vscode from 'vscode';
import { getOrCreateItemTree } from '../tree';

suite('getOrCreateItemTree', () => {
    let controller: vscode.TestController;
    let workspaceFolder: vscode.WorkspaceFolder;

    setup(() => {
        controller = vscode.tests.createTestController('promptarchitect', 'Prompt Architect');
        workspaceFolder = vscode.workspace.workspaceFolders![0];
    });

    teardown(() => {
        controller.dispose();
    });

    test('root folder', () => {
        const uri = '/tests';
        const item = getOrCreateItemTree(controller, workspaceFolder, vscode.Uri.parse(uri));

        assert.strictEqual(item.label, 'tests');
        assert.strictEqual(item.parent, undefined);
    });

    test('nested folder', () => {
        const uri = '/tests/nested';
        const item = getOrCreateItemTree(controller, workspaceFolder, vscode.Uri.parse(uri));

        assert.strictEqual(item.label, 'nested');
        assert.strictEqual(item.parent!.label, 'tests');
        assert.strictEqual(item.parent!.parent, undefined);
    });

    test('prompt file path', () => {
        const uri = '/tests/nested/test01.prompt';
        const item = getOrCreateItemTree(controller, workspaceFolder, vscode.Uri.parse(uri));

        assert.strictEqual(item.label, 'test01.prompt');
        assert.strictEqual(item.parent!.label, 'nested');
        assert.strictEqual(item.parent!.parent!.label, 'tests');
        assert.strictEqual(item.parent!.parent!.parent, undefined);
    });
});
