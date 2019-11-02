package org.brtracer.sourcecode.ast;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.CompilationUnit;

public class ASTCreator {

	private String content = null;

	public void getFileContent(File file) {
		this.getFileContent(file.getAbsolutePath());
	}

	//��ȡ�ļ�����
	public void getFileContent(String absoluteFilePath) {
		try (BufferedReader reader = new BufferedReader(new FileReader(absoluteFilePath))){
			StringBuffer contentBuffer = new StringBuffer();
			String line = null;
			while ((line = reader.readLine()) != null)
				contentBuffer.append(line+"\r\n");
			content = contentBuffer.toString();
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}
	
	//��ȡ�ļ���Ӧ��CompilationUnit
	public CompilationUnit getCompilationUnit() {
		ASTParser parser = ASTParser.newParser(AST.JLS3);
		parser.setSource(content.toCharArray());
		CompilationUnit cu = (CompilationUnit) parser.createAST(null);
		return cu;
	}
}
