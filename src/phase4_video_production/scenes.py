from manim import *
import json

class MathExplanationScene(Scene):
    def __init__(self, script_data: dict, **kwargs):
        super().__init__(**kwargs)
        self.script = script_data
        
    def construct(self):
        # 1. Introducción
        self.show_introduction()
        self.wait(1)
        self.clear()
        
        # 2. Identificación del error
        self.show_error_identification()
        self.wait(1)
        self.clear()
        
        # 3. Explicación del concepto
        self.show_concept_explanation()
        self.wait(1)
        self.clear()
        
        # 4. Solución paso a paso
        self.show_step_by_step()
        self.wait(1)
        self.clear()
        
        # 5. Cierre
        self.show_closing()
        self.wait(2)
    
    def show_introduction(self):
        """Animación de introducción"""
        intro_text = Text(
            self.script['introduccion']['texto'],
            font_size=36
        ).scale(0.8)
        
        self.play(Write(intro_text), run_time=3)
        self.wait(self.script['introduccion']['duracion_estimada'] - 3)
    
    def show_error_identification(self):
        """Muestra el error del estudiante"""
        error_text = Text(
            self.script['identificacion_error']['texto'],
            font_size=32,
            color=RED
        ).scale(0.7)
        
        self.play(FadeIn(error_text), run_time=2)
        self.wait(self.script['identificacion_error']['duracion_estimada'] - 2)
    
    def show_concept_explanation(self):
        """Explicación del concepto"""
        concept = self.script['explicacion_concepto']
        
        title = Text("Concepto:", font_size=40, color=BLUE).to_edge(UP)
        explanation = Text(
            concept['texto'],
            font_size=28
        ).scale(0.8).next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), run_time=1)
        self.play(FadeIn(explanation), run_time=2)
        
        # Analogía si existe
        if concept.get('analogia'):
            self.wait(1)
            analogy = Text(
                concept['analogia'],
                font_size=24,
                color=YELLOW
            ).scale(0.7).to_edge(DOWN)
            self.play(FadeIn(analogy), run_time=2)
        
        self.wait(concept['duracion_estimada'] - 4)
    
    def show_step_by_step(self):
        """Muestra la solución paso a paso"""
        title = Text("Solución:", font_size=40, color=GREEN).to_edge(UP)
        self.play(Write(title), run_time=1)
        
        y_position = 2
        for step in self.script['solucion_paso_a_paso']:
            step_text = Text(
                f"{step['paso_numero']}. {step['texto']}",
                font_size=28
            ).scale(0.7)
            step_text.move_to(UP * y_position)
            
            # Operación matemática
            operation = MathTex(
                step['operacion'],
                font_size=48,
                color=BLUE
            ).next_to(step_text, DOWN, buff=0.3)
            
            self.play(
                Write(step_text),
                FadeIn(operation),
                run_time=2
            )
            self.wait(step['duracion_estimada'] - 2)
            
            y_position -= 1.5
    
    def show_closing(self):
        """Mensaje de cierre"""
        closing = Text(
            self.script['cierre']['texto'],
            font_size=36,
            color=GREEN
        ).scale(0.8)
        
        self.play(
            Write(closing),
            closing.animate.scale(1.2),
            run_time=3
        )