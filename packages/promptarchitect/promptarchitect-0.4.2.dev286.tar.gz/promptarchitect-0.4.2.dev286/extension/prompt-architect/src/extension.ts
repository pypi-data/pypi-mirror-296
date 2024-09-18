// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { InteractiveTestSession } from './session';

/**
 * Activate the extension in vscode.
 * @param context The extension context
 */
export function activate(context: vscode.ExtensionContext) {
	console.log("Prompt Architect extension activated");

	const testController = vscode.tests.createTestController('promptarchitectTestController', 'Prompt architect');
	const testSession = new InteractiveTestSession(testController);

	context.subscriptions.push(testSession);
}

/**
 * Deactivate the extension
 */
export function deactivate() { }





