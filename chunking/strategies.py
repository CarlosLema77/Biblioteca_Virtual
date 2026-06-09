"""
S: Cada clase tiene una sola responsabilidad — implementar su estrategia
O: Para agregar una nueva estrategia, solo se agrega una clase nueva
L: Todas las estrategias heredan de ChunkingStrategy y son intercambiables
"""
from abc import ABC, abstractmethod
from langchain_text_splitters import RecursiveCharacterTextSplitter, NLTKTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np


class ChunkingStrategy(ABC):
    """
    Clase base abstracta — define la interfaz común
    L: Cualquier estrategia puede reemplazar a otra sin romper el sistema
    """
    @abstractmethod
    def split(self, texto: str) -> list[str]:
        """Divide el texto en chunks y retorna lista de strings"""
        pass

    def nombre(self) -> str:
        return self.__class__.__name__


class FixedSizeChunking(ChunkingStrategy):
    """
    Estrategia A: Divide el texto en fragmentos de N tokens con overlap
    Ideal para: artículos académicos largos y homogéneos
    """
    def __init__(self, chunk_size: int = 256, overlap: int = 32):
        self.chunk_size = chunk_size
        self.overlap    = overlap
        self.splitter   = RecursiveCharacterTextSplitter(
            chunk_size        = chunk_size,
            chunk_overlap     = overlap,
            length_function   = len,
            separators        = ["\n\n", "\n", " ", ""]
        )

    def split(self, texto: str) -> list[str]:
        chunks = self.splitter.split_text(texto)
        return [c.strip() for c in chunks if len(c.strip()) > 20]

    def nombre(self) -> str:
        return "fixed-size"
    
class SentenceAwareChunking(ChunkingStrategy):
    """
    Estrategia B: Respeta límites de oraciones, nunca corta en medio de una frase
    Ideal para: novelas, cuentos, textos narrativos
    """
    def __init__(self, max_oraciones: int = 5, overlap_oraciones: int = 1):
        self.max_oraciones     = max_oraciones
        self.overlap_oraciones = overlap_oraciones

    def _split_oraciones(self, texto: str) -> list[str]:
        """Divide texto en oraciones usando puntuación"""
        import re
        oraciones = re.split(r'(?<=[.!?])\s+', texto.strip())
        return [o.strip() for o in oraciones if len(o.strip()) > 10]

    def split(self, texto: str) -> list[str]:
        oraciones = self._split_oraciones(texto)
        chunks    = []
        i         = 0

        while i < len(oraciones):
            grupo = oraciones[i : i + self.max_oraciones]
            chunk = " ".join(grupo)
            if len(chunk.strip()) > 20:
                chunks.append(chunk.strip())
            i += self.max_oraciones - self.overlap_oraciones

        return chunks

    def nombre(self) -> str:
        return "sentence-aware"
    
class SemanticChunking(ChunkingStrategy):
    """
    Estrategia C: Agrupa oraciones por similitud semántica usando embeddings
    Ideal para: papers, textos con cambios de tema
    """
    def __init__(self, umbral_similitud: float = 0.80, modelo: str = "all-MiniLM-L6-v2"):
        self.umbral_similitud = umbral_similitud
        self.modelo           = SentenceTransformer(modelo)

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calcula similitud coseno entre dos vectores"""
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def _split_oraciones(self, texto: str) -> list[str]:
        import re
        oraciones = re.split(r'(?<=[.!?])\s+', texto.strip())
        return [o.strip() for o in oraciones if len(o.strip()) > 10]

    def split(self, texto: str) -> list[str]:
        oraciones = self._split_oraciones(texto)
        if len(oraciones) == 0:
            return []

        # Generar embedding para cada oración
        embeddings = self.modelo.encode(oraciones, show_progress_bar=False)

        chunks        = []
        grupo_actual  = [oraciones[0]]

        for i in range(1, len(oraciones)):
            # Comparar oración actual con la anterior
            sim = self._cosine_similarity(embeddings[i], embeddings[i - 1])

            if sim >= self.umbral_similitud:
                # Son similares — agregar al grupo actual
                grupo_actual.append(oraciones[i])
            else:
                # Cambio de tema — guardar grupo y empezar uno nuevo
                chunk = " ".join(grupo_actual)
                if len(chunk.strip()) > 20:
                    chunks.append(chunk.strip())
                grupo_actual = [oraciones[i]]

        # Guardar el último grupo
        if grupo_actual:
            chunk = " ".join(grupo_actual)
            if len(chunk.strip()) > 20:
                chunks.append(chunk.strip())

        return chunks

    def nombre(self) -> str:
        return "semantic"