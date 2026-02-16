#!/usr/bin/env python3
"""
Mobile Wizard — Scaffold React Native / Expo projects.

Usage:
    python mobile_init.py --name "MyApp" --type expo-router
"""

import argparse
import os
from pathlib import Path

FILE_STRUCTURE = {
    "app/_layout.tsx": """import { Stack } from 'expo-router';

export default function Layout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
    </Stack>
  );
}""",
    "app/(tabs)/_layout.tsx": """import { Tabs } from 'expo-router';

export default function TabLayout() {
  return (
    <Tabs>
      <Tabs.Screen name="index" options={{ title: 'Home' }} />
      <Tabs.Screen name="settings" options={{ title: 'Settings' }} />
    </Tabs>
  );
}""",
    "app/(tabs)/index.tsx": """import { View, Text } from 'react-native';

export default function Home() {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Home Screen</Text>
    </View>
  );
}""",
    "app/(tabs)/settings.tsx": """import { View, Text } from 'react-native';

export default function Settings() {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Settings Screen</Text>
    </View>
  );
}"""
}

def generate_expo_router(name):
    print(f"📱 Scaffolding Expo Router for {name}...")
    
    # Simulate creation (in real life, we'd run npx create-expo-app)
    # But here we assume project exists or we create the structure
    
    for path, content in FILE_STRUCTURE.items():
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created {path}")

    print("\nNext Steps:")
    print("1. npx expo install expo-router react-native-safe-area-context react-native-screens expo-linking expo-constants expo-status-bar")
    print("2. npx expo start")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="MyApp")
    parser.add_argument("--type", default="expo-router")
    args = parser.parse_args()
    
    if args.type == "expo-router":
        generate_expo_router(args.name)

if __name__ == "__main__":
    main()
