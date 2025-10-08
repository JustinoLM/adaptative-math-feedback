import os
import json
import subprocess
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class ManimRenderer:
    def __init__(self):
        # Obtener raíz del proyecto (2 niveles arriba desde este archivo)
        project_root = Path(__file__).parent.parent.parent
    
        self.output_dir = project_root / "output" / "videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
        self.temp_dir = project_root / "output" / "temp"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
        self.quality = os.getenv("MANIM_QUALITY", "medium_quality")
    
        logger.info(f"Directorio de salida: {self.output_dir}")
        logger.info(f"Directorio temporal: {self.temp_dir}")
    
    def render(self, script_data: dict, video_name: str = "explanation") -> Path:
        """Renderiza video con MANIM"""
    
        logger.info(f"Iniciando renderizado de video: {video_name}")
    
        # Guardar script como JSON temporal
        script_file = self.temp_dir / f"{video_name}_script.json"
        with open(script_file, 'w', encoding='utf-8') as f:
            json.dump(script_data, f, ensure_ascii=False, indent=2)
    
        # Crear archivo Python temporal con la escena
        scene_file = self.temp_dir / f"{video_name}_scene.py"
        self._create_scene_file(scene_file, script_file)
    
        # Comando MANIM - usar ruta relativa al archivo
        quality_flag = self._get_quality_flag()
    
        cmd = [
            "manim",
            quality_flag,
            f"{video_name}_scene.py",  # Solo el nombre del archivo
            "MathExplanationScene",
            "-o", f"{video_name}.mp4"
        ]
    
        logger.info(f"Ejecutando: {' '.join(cmd)}")
        logger.info(f"Directorio de trabajo: {self.temp_dir}")
    
        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.temp_dir),  # Trabajar desde temp_dir
                capture_output=True,
                text=True,
                timeout=300
            )
        
            if result.returncode != 0:
                logger.error(f"Error en MANIM: {result.stderr}")
                raise RuntimeError(f"MANIM falló: {result.stderr}")
        
            # Buscar video generado
            media_dir = self.temp_dir / "media" / "videos" / f"{video_name}_scene"
        
            # Buscar en subdirectorios de calidad
            for quality_dir in media_dir.glob("*"):
                if quality_dir.is_dir():
                    video_file = quality_dir / f"{video_name}.mp4"
                    if video_file.exists():
                        # Mover al directorio final
                        final_path = self.output_dir / f"{video_name}.mp4"
                        import shutil
                        shutil.copy(video_file, final_path)
                        logger.info(f"Video generado: {final_path}")
                        return final_path
        
            raise FileNotFoundError(f"Video no encontrado en {media_dir}")
            
        except subprocess.TimeoutExpired:
            logger.error("Timeout en renderizado")
            raise
        except Exception as e:
            logger.error(f"Error renderizando: {e}")
            raise
    
    def _create_scene_file(self, scene_file: Path, script_file: Path):
        """Crea archivo Python con la escena mejorada"""
        code = f'''
from manim import *
import json

with open("{script_file}", "r", encoding="utf-8") as f:
    SCRIPT_DATA = json.load(f)

class MathExplanationScene(Scene):
    def construct(self):
        # 1. Introducción
        intro_lines = SCRIPT_DATA["introduccion"]["texto"].split(". ")
        intro = VGroup(*[Text(line, font_size=36) for line in intro_lines])
        intro.arrange(DOWN, buff=0.3).scale(0.7)
        self.play(Write(intro), run_time=3)
        self.wait(SCRIPT_DATA["introduccion"]["duracion_estimada"] - 3)
        self.clear()
        
        # 2. Identificar error
        error_lines = SCRIPT_DATA["identificacion_error"]["texto"].split(". ")
        error = VGroup(*[Text(line, font_size=32, color=RED) for line in error_lines])
        error.arrange(DOWN, buff=0.3).scale(0.6)
        self.play(FadeIn(error), run_time=2)
        self.wait(SCRIPT_DATA["identificacion_error"]["duracion_estimada"] - 2)
        self.clear()
        
        # 3. Explicación con visuales
        title = Text("Concepto:", font_size=40, color=BLUE).to_edge(UP)
        concept_lines = SCRIPT_DATA["explicacion_concepto"]["texto"].split(". ")
        concept = VGroup(*[Text(line, font_size=28) for line in concept_lines])
        concept.arrange(DOWN, buff=0.3).scale(0.6).next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), run_time=1)
        self.play(FadeIn(concept), run_time=2)
        self.wait(SCRIPT_DATA["explicacion_concepto"]["duracion_estimada"] - 3)
        self.clear()
        
        # 4. Solución paso a paso con visuales
        title = Text("Solución:", font_size=40, color=GREEN).to_edge(UP)
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        for i, step in enumerate(SCRIPT_DATA["solucion_paso_a_paso"]):
            self.clear()
            title = Text("Solución:", font_size=40, color=GREEN).to_edge(UP)
            self.add(title)
            
            # Texto del paso
            step_lines = step["texto"].split(". ")
            step_text = VGroup(*[Text(line, font_size=26) for line in step_lines])
            step_text.arrange(DOWN, buff=0.2).scale(0.7).move_to(UP * 2)
            
            self.play(Write(step_text), run_time=1.5)
            self.wait(0.5)
            
            # Extraer números de la operación
            operation_str = step["operacion"]
            
            # Mostrar operación matemática grande
            operation = MathTex(operation_str, font_size=100, color=YELLOW)
            operation.move_to(ORIGIN)
            self.play(FadeIn(operation, scale=1.2), run_time=1.5)
            
            # Si tiene números, mostrar representación visual
            if "+" in operation_str or "-" in operation_str or "=" in operation_str:
                self._show_visual_representation(operation_str)
            
            self.wait(step["duracion_estimada"] - 3)
        
        # 5. Mostrar RESULTADO FINAL destacado
        self.clear()
        result_title = Text("¡Resultado Final!", font_size=45, color=GREEN).to_edge(UP)
        
        # Extraer resultado del último paso
        last_step = SCRIPT_DATA["solucion_paso_a_paso"][-1]["operacion"]
        if "=" in last_step:
            result = last_step.split("=")[-1].strip()
        else:
            result = last_step
        
        result_box = Rectangle(width=4, height=2, color=GREEN, fill_opacity=0.2)
        result_text = MathTex(result, font_size=120, color=YELLOW)
        result_group = VGroup(result_box, result_text)
        
        self.play(Write(result_title), run_time=1)
        self.play(
            Create(result_box),
            Write(result_text),
            run_time=2
        )
        self.play(result_group.animate.scale(1.1), run_time=0.5)
        self.play(result_group.animate.scale(1/1.1), run_time=0.5)
        self.wait(2)
        self.clear()
        
        # 6. Cierre
        closing_lines = SCRIPT_DATA["cierre"]["texto"].split(". ")
        closing = VGroup(*[Text(line, font_size=36, color=GREEN) for line in closing_lines])
        closing.arrange(DOWN, buff=0.3).scale(0.7)
        
        self.play(Write(closing), run_time=2)
        self.play(closing.animate.scale(1.15), run_time=0.5)
        self.play(closing.animate.scale(1/1.15), run_time=0.5)
        self.wait(2)
    
    def _show_visual_representation(self, operation_str):
        """Muestra representación visual con figuras"""
        try:
            # Intentar parsear números
            parts = operation_str.replace(" ", "").split("=")[0]
            
            if "+" in parts:
                nums = parts.split("+")
                if len(nums) == 2:
                    num1 = int(float(nums[0]))
                    num2 = int(float(nums[1]))
                    
                    # Limitar cantidad de figuras
                    if num1 <= 20 and num2 <= 20:
                        # Grupo 1
                        circles1 = VGroup(*[Circle(radius=0.15, color=BLUE, fill_opacity=0.7) 
                                          for _ in range(num1)])
                        circles1.arrange_in_grid(rows=min(4, num1), buff=0.1).scale(0.8)
                        circles1.shift(LEFT * 3 + DOWN * 1)
                        
                        # Signo +
                        plus = MathTex("+", font_size=60, color=WHITE).next_to(circles1, RIGHT, buff=0.5)
                        
                        # Grupo 2
                        circles2 = VGroup(*[Circle(radius=0.15, color=RED, fill_opacity=0.7) 
                                          for _ in range(num2)])
                        circles2.arrange_in_grid(rows=min(4, num2), buff=0.1).scale(0.8)
                        circles2.next_to(plus, RIGHT, buff=0.5)
                        
                        self.play(
                            FadeIn(circles1),
                            FadeIn(plus),
                            FadeIn(circles2),
                            run_time=2
                        )
                        self.wait(1)
        except:
            pass  # Si no se puede parsear, solo muestra la operación
'''
    
        with open(scene_file, 'w', encoding='utf-8') as f:
            f.write(code)
    
    def _get_quality_flag(self) -> str:
        """Mapea calidad a flag de MANIM"""
        quality_map = {
            "low": "-ql",
            "medium": "-qm",
            "high": "-qh",
            "production": "-qk"
        }
        return quality_map.get(self.quality, "-qm")


if __name__ == "__main__":
    # Cargar guión de ejemplo
    script_path = Path("output/temp/test_script.json")
    
    if not script_path.exists():
        print("Primero ejecuta script_builder.py para generar un guión")
        exit(1)
    
    with open(script_path, 'r', encoding='utf-8') as f:
        script = json.load(f)
    
    renderer = ManimRenderer()
    video_path = renderer.render(script, "test_video")
    print(f"\n✅ Video generado: {video_path}")