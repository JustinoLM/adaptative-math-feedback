
from manim import *
import json

with open("/Users/justino/Documents/Universidad/Tesis/Desarrollo/MANIM PIPELINE/adaptative-math-feedback/output/temp/test_video_script.json", "r", encoding="utf-8") as f:
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
            operation = MathTex(operation_str, font_size=70, color=YELLOW)
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
        result_text = MathTex(result, font_size=90, color=YELLOW)
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
