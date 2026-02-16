# Mobile Developer - iOS/Android (React Native/Expo).

# Mobile Developer Workflow

## Core Principles
1.  **Universal Design**: Use `ui-ux-pro-max` logic but adapt for small screens.
2.  **Native Performance**: Avoid heavy bridges given the "Vibe" constraint. 
3.  **Token Saver**: Use `diff-applier` for screen updates.

## Workflow

### Step 1: Scaffold App (Zero Token)
Generate standard Expo Router structure.
```bash
python .agent/skills/mobile-wizard/scripts/mobile_init.py --name "VibeApp" --type expo-router
```

### Step 2: Implement Screens
1.  Read design system context.
2.  Generate screen code via LLM (minified context).
3.  Apply using patches.

### Step 3: Test on Device
(Manual step: `npx expo start`)
