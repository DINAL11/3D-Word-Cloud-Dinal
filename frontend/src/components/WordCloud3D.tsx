import { useRef, useMemo, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text } from '@react-three/drei';
import * as THREE from 'three';

interface WordData {
  word: string;
  weight: number;
  frequency: number;
}

interface WordCloud3DProps {
  words: WordData[];
}

interface Word3DProps {
  word: string;
  position: [number, number, number];
  size: number;
  weight: number;
  frequency: number;
}

// Individual 3D word component
function Word3D({ word, position, size, weight, frequency }: Word3DProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  // Animate word entrance
  useFrame((state) => {
    if (meshRef.current) {
      const time = state.clock.elapsedTime;
      
      // Gentle floating animation
      meshRef.current.position.y = position[1] + Math.sin(time + position[0]) * 0.1;
      
      // Slight rotation
      meshRef.current.rotation.y = Math.sin(time * 0.5 + position[0]) * 0.1;
    }
  });

  // Color based on weight (blue to red gradient)
  const color = useMemo(() => {
    const hue = (1 - weight) * 0.6; // 0.6 (blue) to 0 (red)
    return new THREE.Color().setHSL(hue, 0.8, 0.6);
  }, [weight]);

  const displayWord = word.replace(/_/g, ' ');

  return (
    <group position={position} ref={meshRef}>
      <Text
        fontSize={size}
        color={color}
        anchorX="center"
        anchorY="middle"
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
        outlineWidth={hovered ? 0.01 : 0}
        outlineColor="#ffffff"
      >
        {displayWord}
      </Text>
      
      {hovered && (
        <Text
          position={[0, -size * 0.8, 0]}
          fontSize={size * 0.3}
          color="#ffffff"
          anchorX="center"
          anchorY="middle"
        >
          {`${frequency}x | ${Math.round(weight * 100)}%`}
        </Text>
      )}
    </group>
  );
}

// Main word cloud component
function WordCloud({ words }: WordCloud3DProps) {
  // Generate positions for words in 3D space
  const wordPositions = useMemo(() => {
    return words.map((word, index) => {
      // Use spherical distribution for natural-looking cloud
      const phi = Math.acos(-1 + (2 * index) / words.length);
      const theta = Math.sqrt(words.length * Math.PI) * phi;
      
      // Scale radius based on weight (more important words closer to center)
      const radius = 5 + (1 - word.weight) * 3;
      
      const x = radius * Math.cos(theta) * Math.sin(phi);
      const y = radius * Math.sin(theta) * Math.sin(phi);
      const z = radius * Math.cos(phi);
      
      // Size based on weight
      const size = 0.2 + word.weight * 0.8;
      
      return {
        word: word.word,
        position: [x, y, z] as [number, number, number],
        size,
        weight: word.weight,
        frequency: word.frequency,
      };
    });
  }, [words]);

  return (
    <group>
      {wordPositions.map((wordData, index) => (
        <Word3D
          key={`${wordData.word}-${index}`}
          word={wordData.word}
          position={wordData.position}
          size={wordData.size}
          weight={wordData.weight}
          frequency={wordData.frequency}
        />
      ))}
    </group>
  );
}

// Main exported component
export default function WordCloud3D({ words }: WordCloud3DProps) {
  return (
    <Canvas
      camera={{ position: [0, 0, 15], fov: 60 }}
      style={{ background: 'linear-gradient(to bottom, #1a1a2e 0%, #0f3460 100%)' }}
    >
      {/* Lighting */}
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} intensity={1} />
      <pointLight position={[-10, -10, -10]} intensity={0.5} />
      
      {/* Word cloud */}
      <WordCloud words={words} />
      
      {/* Camera controls */}
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        rotateSpeed={0.5}
        zoomSpeed={0.8}
        minDistance={5}
        maxDistance={30}
      />
    </Canvas>
  );
}