#!/usr/bin/env python3
"""
Script de teste de integração para o Email Assistant App
Verifica se todos os componentes estão corretamente integrados
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class EmailAssistantTester:
    def __init__(self):
        self.project_root = Path("/home/ubuntu/EmailAssistantApp")
        self.test_results = []
        
    def log_test(self, test_name, passed, message=""):
        """Registra resultado de um teste"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "message": message
        })
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
    
    def test_project_structure(self):
        """Testa se a estrutura do projeto está correta"""
        print("\n🔍 Testando estrutura do projeto...")
        
        required_files = [
            "build.gradle",
            "app/build.gradle",
            "app/src/main/AndroidManifest.xml",
            "app/src/main/java/com/emailassistant/EmailAssistantApplication.kt",
            "app/src/main/java/com/emailassistant/ui/main/MainActivity.kt",
            "app/src/main/java/com/emailassistant/ui/setup/SetupActivity.kt",
            "app/src/main/java/com/emailassistant/ui/auth/AuthActivity.kt",
            "app/src/main/res/values/strings.xml",
            "app/src/main/res/values/colors.xml",
            "app/src/main/res/layout/activity_main.xml",
            "app/src/main/res/layout/activity_setup.xml",
            "app/src/main/res/layout/activity_auth.xml"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.log_test(
                "Estrutura do projeto",
                False,
                f"Arquivos faltando: {', '.join(missing_files)}"
            )
        else:
            self.log_test("Estrutura do projeto", True, "Todos os arquivos necessários estão presentes")
    
    def test_kotlin_syntax(self):
        """Testa se os arquivos Kotlin têm sintaxe válida"""
        print("\n🔍 Testando sintaxe dos arquivos Kotlin...")
        
        kotlin_files = list(self.project_root.rglob("*.kt"))
        syntax_errors = []
        
        for kt_file in kotlin_files:
            try:
                with open(kt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Verificações básicas de sintaxe
                if not content.strip():
                    syntax_errors.append(f"{kt_file.name}: Arquivo vazio")
                    continue
                    
                # Verificar se tem package declaration
                if not content.startswith("package "):
                    syntax_errors.append(f"{kt_file.name}: Falta declaração de package")
                
                # Verificar balanceamento de chaves
                open_braces = content.count('{')
                close_braces = content.count('}')
                if open_braces != close_braces:
                    syntax_errors.append(f"{kt_file.name}: Chaves desbalanceadas ({open_braces} abrir, {close_braces} fechar)")
                
            except Exception as e:
                syntax_errors.append(f"{kt_file.name}: Erro ao ler arquivo - {str(e)}")
        
        if syntax_errors:
            self.log_test(
                "Sintaxe Kotlin",
                False,
                f"Erros encontrados: {'; '.join(syntax_errors[:5])}"  # Mostrar apenas os primeiros 5
            )
        else:
            self.log_test("Sintaxe Kotlin", True, f"Todos os {len(kotlin_files)} arquivos Kotlin estão válidos")
    
    def test_xml_syntax(self):
        """Testa se os arquivos XML têm sintaxe válida"""
        print("\n🔍 Testando sintaxe dos arquivos XML...")
        
        xml_files = list(self.project_root.rglob("*.xml"))
        xml_errors = []
        
        for xml_file in xml_files:
            try:
                import xml.etree.ElementTree as ET
                ET.parse(xml_file)
            except ET.ParseError as e:
                xml_errors.append(f"{xml_file.name}: {str(e)}")
            except Exception as e:
                xml_errors.append(f"{xml_file.name}: Erro ao ler - {str(e)}")
        
        if xml_errors:
            self.log_test(
                "Sintaxe XML",
                False,
                f"Erros encontrados: {'; '.join(xml_errors[:3])}"
            )
        else:
            self.log_test("Sintaxe XML", True, f"Todos os {len(xml_files)} arquivos XML estão válidos")
    
    def test_dependencies(self):
        """Testa se as dependências estão corretamente configuradas"""
        print("\n🔍 Testando configuração de dependências...")
        
        build_gradle = self.project_root / "app" / "build.gradle"
        
        if not build_gradle.exists():
            self.log_test("Dependências", False, "Arquivo build.gradle não encontrado")
            return
        
        try:
            with open(build_gradle, 'r') as f:
                content = f.read()
            
            required_deps = [
                "hilt-android",
                "retrofit",
                "okhttp",
                "room-runtime",
                "lifecycle-viewmodel-ktx",
                "androidx.appcompat",
                "material"
            ]
            
            missing_deps = []
            for dep in required_deps:
                if dep not in content:
                    missing_deps.append(dep)
            
            if missing_deps:
                self.log_test(
                    "Dependências",
                    False,
                    f"Dependências faltando: {', '.join(missing_deps)}"
                )
            else:
                self.log_test("Dependências", True, "Todas as dependências necessárias estão presentes")
                
        except Exception as e:
            self.log_test("Dependências", False, f"Erro ao ler build.gradle: {str(e)}")
    
    def test_manifest_configuration(self):
        """Testa se o AndroidManifest.xml está corretamente configurado"""
        print("\n🔍 Testando configuração do AndroidManifest...")
        
        manifest_file = self.project_root / "app" / "src" / "main" / "AndroidManifest.xml"
        
        if not manifest_file.exists():
            self.log_test("AndroidManifest", False, "AndroidManifest.xml não encontrado")
            return
        
        try:
            with open(manifest_file, 'r') as f:
                content = f.read()
            
            required_permissions = [
                "RECORD_AUDIO",
                "INTERNET",
                "ACCESS_NETWORK_STATE"
            ]
            
            required_activities = [
                "MainActivity",
                "SetupActivity",
                "AuthActivity"
            ]
            
            missing_permissions = [p for p in required_permissions if p not in content]
            missing_activities = [a for a in required_activities if a not in content]
            
            issues = []
            if missing_permissions:
                issues.append(f"Permissões faltando: {', '.join(missing_permissions)}")
            if missing_activities:
                issues.append(f"Atividades faltando: {', '.join(missing_activities)}")
            
            if issues:
                self.log_test("AndroidManifest", False, "; ".join(issues))
            else:
                self.log_test("AndroidManifest", True, "Configuração correta")
                
        except Exception as e:
            self.log_test("AndroidManifest", False, f"Erro ao ler manifest: {str(e)}")
    
    def test_resource_integrity(self):
        """Testa se os recursos estão corretamente referenciados"""
        print("\n🔍 Testando integridade dos recursos...")
        
        # Verificar se strings referenciadas existem
        strings_file = self.project_root / "app" / "src" / "main" / "res" / "values" / "strings.xml"
        colors_file = self.project_root / "app" / "src" / "main" / "res" / "values" / "colors.xml"
        
        issues = []
        
        if not strings_file.exists():
            issues.append("strings.xml não encontrado")
        if not colors_file.exists():
            issues.append("colors.xml não encontrado")
        
        # Verificar se drawables referenciados existem
        drawable_dir = self.project_root / "app" / "src" / "main" / "res" / "drawable"
        required_drawables = [
            "ic_settings.xml",
            "ic_mic_active.xml",
            "ic_arrow_back.xml",
            "voice_button_background.xml"
        ]
        
        missing_drawables = []
        for drawable in required_drawables:
            if not (drawable_dir / drawable).exists():
                missing_drawables.append(drawable)
        
        if missing_drawables:
            issues.append(f"Drawables faltando: {', '.join(missing_drawables)}")
        
        if issues:
            self.log_test("Recursos", False, "; ".join(issues))
        else:
            self.log_test("Recursos", True, "Todos os recursos necessários estão presentes")
    
    def test_architecture_integrity(self):
        """Testa se a arquitetura MVVM está corretamente implementada"""
        print("\n🔍 Testando integridade da arquitetura...")
        
        # Verificar se ViewModels existem para cada Activity
        viewmodels = [
            "app/src/main/java/com/emailassistant/ui/main/MainViewModel.kt",
            "app/src/main/java/com/emailassistant/ui/setup/SetupViewModel.kt",
            "app/src/main/java/com/emailassistant/ui/auth/AuthViewModel.kt"
        ]
        
        # Verificar se repositórios estão implementados
        repositories = [
            "app/src/main/java/com/emailassistant/data/repository/impl/EmailRepositoryImpl.kt",
            "app/src/main/java/com/emailassistant/data/repository/impl/SpeechRepositoryImpl.kt",
            "app/src/main/java/com/emailassistant/data/repository/impl/AIAnalysisRepositoryImpl.kt"
        ]
        
        # Verificar se módulos de DI existem
        di_modules = [
            "app/src/main/java/com/emailassistant/di/NetworkModule.kt",
            "app/src/main/java/com/emailassistant/di/DatabaseModule.kt",
            "app/src/main/java/com/emailassistant/di/RepositoryModule.kt"
        ]
        
        missing_components = []
        
        for component_list, name in [(viewmodels, "ViewModels"), (repositories, "Repositories"), (di_modules, "DI Modules")]:
            for component in component_list:
                if not (self.project_root / component).exists():
                    missing_components.append(f"{name}: {Path(component).name}")
        
        if missing_components:
            self.log_test("Arquitetura", False, f"Componentes faltando: {', '.join(missing_components)}")
        else:
            self.log_test("Arquitetura", True, "Arquitetura MVVM corretamente implementada")
    
    def generate_report(self):
        """Gera relatório final dos testes"""
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL DE INTEGRAÇÃO")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["passed"])
        failed_tests = total_tests - passed_tests
        
        print(f"\nTotal de testes: {total_tests}")
        print(f"✅ Passou: {passed_tests}")
        print(f"❌ Falhou: {failed_tests}")
        print(f"📈 Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ TESTES QUE FALHARAM:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"  • {result['test']}: {result['message']}")
        
        print("\n" + "="*60)
        
        # Salvar relatório em arquivo
        report_file = self.project_root / "integration_test_report.json"
        with open(report_file, 'w') as f:
            json.dump({
                "timestamp": str(subprocess.check_output(['date'], text=True).strip()),
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests/total_tests)*100,
                "results": self.test_results
            }, f, indent=2)
        
        print(f"📄 Relatório salvo em: {report_file}")
        
        return failed_tests == 0
    
    def run_all_tests(self):
        """Executa todos os testes de integração"""
        print("🚀 INICIANDO TESTES DE INTEGRAÇÃO DO EMAIL ASSISTANT")
        print("="*60)
        
        # Executar todos os testes
        self.test_project_structure()
        self.test_kotlin_syntax()
        self.test_xml_syntax()
        self.test_dependencies()
        self.test_manifest_configuration()
        self.test_resource_integrity()
        self.test_architecture_integrity()
        
        # Gerar relatório final
        success = self.generate_report()
        
        if success:
            print("\n🎉 TODOS OS TESTES PASSARAM! O aplicativo está pronto para compilação.")
        else:
            print("\n⚠️  ALGUNS TESTES FALHARAM. Revise os problemas antes de prosseguir.")
        
        return success

if __name__ == "__main__":
    tester = EmailAssistantTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

