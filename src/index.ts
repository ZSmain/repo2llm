#!/usr/bin/env bun

import { Command } from 'commander';
import * as fs from 'fs';
import * as path from 'path';

function parseGitignore(repoPath: string): string[] {
	const gitignorePath = path.join(repoPath, '.gitignore');
	let patterns: string[] = [];

	try {
		const content = fs.readFileSync(gitignorePath, 'utf-8');
		patterns = content
			.split('\n')
			.map(line => line.trim())
			.filter(line => line && !line.startsWith('#'))
			.map(line => line.replace(/^\/+/, '')) // Remove leading slashes
			.filter(line => !line.startsWith('!')); // Ignore negation patterns for now
	} catch {
		// If no .gitignore, continue with empty array
	}

	// Add common exclusions that are typically not in .gitignore
	const commonExclusions = [
		'.git',
		'node_modules',
		'.venv',
		'venv',
		'env',
		'__pycache__',
		'.pytest_cache',
		'.DS_Store',
		'Thumbs.db',
		'pnpm-lock.yaml',
		'bun.lock',
		'yarn.lock',
	];

	return [...patterns, ...commonExclusions];
}

function shouldIgnoreFile(filePath: string, gitignorePatterns: string[], repoPath: string, outputFile?: string): boolean {
	const relativePath = path.relative(repoPath, filePath);
	const fileName = path.basename(filePath);

	// Don't ignore our own output file
	if (outputFile && filePath === path.resolve(outputFile)) {
		return false;
	}

	// Check each gitignore pattern
	for (const pattern of gitignorePatterns) {
		if (pattern.endsWith('/')) {
			// Directory pattern
			const dirPattern = pattern.slice(0, -1);
			if (relativePath.startsWith(dirPattern) || relativePath.includes('/' + dirPattern)) {
				return true;
			}
		} else if (pattern.includes('*')) {
			// Wildcard pattern - simple implementation
			const regexPattern = pattern
				.replace(/\*/g, '.*')
				.replace(/\?/g, '.')
				.replace(/\./g, '\\.');
			const regex = new RegExp(regexPattern);
			if (regex.test(relativePath) || regex.test(fileName)) {
				return true;
			}
		} else {
			// Exact match
			if (relativePath === pattern || fileName === pattern) {
				return true;
			}
		}
	}
	return false;
}

function consolidateFiles(
	repoPath: string,
	outputFile?: string,
	includeExtensions?: string[]
): void {
	const gitignorePatterns = parseGitignore(repoPath);
	const defaultIncludeExtensions = ['.py', '.js', '.ts', '.svelte', '.txt', '.md', '.html', '.css', '.json', '.yml', '.yaml'];

	// Binary/media file extensions that should be excluded
	const binaryExtensions = [
		// Images
		'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico', '.raw',
		// Videos
		'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v',
		// Audio
		'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a',
		// Documents
		'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'
	];

	const finalIncludeExtensions = includeExtensions || defaultIncludeExtensions;

	// Generate default filename if not provided
	let finalOutputFile = outputFile;
	if (!finalOutputFile) {
		const projectName = path.basename(path.resolve(repoPath));
		const currentDate = new Date().toISOString().split('T')[0];
		finalOutputFile = `${projectName}_llm_${currentDate}.txt`;
	}

	const outputStream = fs.createWriteStream(finalOutputFile, { encoding: 'utf-8' });
	const binaryFiles: string[] = [];

	function processDirectory(dirPath: string): void {
		const items = fs.readdirSync(dirPath);

		for (const item of items) {
			const fullPath = path.join(dirPath, item);
			const stat = fs.statSync(fullPath);

			if (stat.isDirectory()) {
				// Skip if ignored by gitignore patterns
				if (!shouldIgnoreFile(fullPath, gitignorePatterns, repoPath, finalOutputFile)) {
					processDirectory(fullPath);
				}
			} else if (stat.isFile()) {
				// Skip if ignored by gitignore patterns
				if (!shouldIgnoreFile(fullPath, gitignorePatterns, repoPath, finalOutputFile)) {
					const ext = path.extname(item);

					// Collect binary/media files for listing (but don't read their content)
					if (binaryExtensions.includes(ext.toLowerCase())) {
						binaryFiles.push(fullPath);
						continue;
					}

					if (finalIncludeExtensions.includes(ext)) {
						try {
							const content = fs.readFileSync(fullPath, 'utf-8');
							outputStream.write(`## FILE: ${fullPath}\n\n`);
							outputStream.write(content);
							outputStream.write('\n\n');
						} catch (error) {
							console.error(`Could not read file ${fullPath}: ${error}`);
						}
					}
				}
			}
		}
	}

	processDirectory(repoPath);

	// Add binary/media files section
	if (binaryFiles.length > 0) {
		outputStream.write('\n\n## BINARY/MEDIA FILES FOUND\n\n');
		outputStream.write('The following binary/media files were found in the repository but not included in the content above:\n\n');
		binaryFiles.forEach(filePath => {
			outputStream.write(`- ${filePath}\n`);
		});
	}

	outputStream.end();
}

function main(): void {
	const program = new Command();

	program
		.name('repo2llm')
		.description('Convert a repository into a single text file for language model processing')
		.version('0.1.0')
		.argument('<repo-path>', 'Path to the repository to process')
		.option('-o, --output <file>', 'Output file path (default: PROJECT_NAME_llm_YYYY-MM-DD.txt)')
		.action((repoPath: string, options: { output?: string }) => {
			const resolvedRepoPath = path.resolve(repoPath);

			if (!fs.existsSync(resolvedRepoPath) || !fs.statSync(resolvedRepoPath).isDirectory()) {
				console.error(`Error: ${resolvedRepoPath} is not a valid directory`);
				process.exit(1);
			}

			console.log(`Processing repository: ${resolvedRepoPath}`);

			const outputFile = options.output;
			if (!outputFile) {
				const projectName = path.basename(resolvedRepoPath);
				const currentDate = new Date().toISOString().split('T')[0];
				const defaultOutputFile = `${projectName}_llm_${currentDate}.txt`;
				console.log(`Output file: ${defaultOutputFile}`);
				consolidateFiles(resolvedRepoPath, defaultOutputFile);
			} else {
				console.log(`Output file: ${outputFile}`);
				consolidateFiles(resolvedRepoPath, outputFile);
			}

			console.log('Repository consolidation complete!');
		});

	program.parse();
}

if (require.main === module) {
	main();
}