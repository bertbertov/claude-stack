# Workflow: build a mobile app

From scratch to shipping in TestFlight / Play Store using the Expo skill suite.

## The prompt to use

```
Build a React Native app for <USE CASE>.

Audience: <who, age, expectations>
Platform: <iOS only | Android only | both>
Stack: Expo SDK 54+, expo-router 6, TypeScript strict, react-native-mmkv for state
Vibe: <one of: AMOLED minimalist | warm editorial | premium-quiet | data-dense>
Key features: <3-5 must-have features>
```

## Routing — Expo specialist skills

The `react-native-apps` skill is the entry point. It points to 13 specialist sub-skills depending on the concern:

| Concern | Specialist |
|---------|-----------|
| Upgrading SDK (54 → 55, dep hell) | upgrading-expo |
| Build/distributing dev clients | expo-dev-client |
| Build & ship to App Store / Play Store | expo-deployment |
| EAS workflow YAML / CI-CD | expo-cicd-workflows |
| OTA update health | eas-update-insights |
| Native modules (Swift / Kotlin / TS) | expo-module |
| API routes (Expo Router + EAS Hosting) | expo-api-routes |
| Universal data fetching, caching | native-data-fetching |
| UI fundamentals + components | building-native-ui |
| Tailwind v4 + NativeWind v5 | expo-tailwind-setup |
| @expo/ui Jetpack Compose interop | expo-ui-jetpack-compose |
| @expo/ui SwiftUI interop | expo-ui-swift-ui |
| DOM components (web-in-webview) | use-dom |

## Stack defaults (from react-native-apps)

| Concern | Default | Why |
|---------|---------|-----|
| Framework | Expo SDK 54+ with expo-router | Native + Web, typed routes, auth gating |
| Language | Strict TypeScript | Mandatory, catches silent bugs |
| Client state | Zustand | 1KB, selector-based, no provider |
| Server state | TanStack Query v5 | Caching, retries, optimistic updates |
| Storage | react-native-mmkv (sync, 30× faster) | Fallback to AsyncStorage |
| Secrets | expo-secure-store | Keychain/Keystore, never AsyncStorage |
| Validation | Zod at API boundaries | Runtime type safety |
| Auth | Clerk or Supabase Auth | Ship fast, custom JWT only if required |
| Animation | Reanimated 3/4 + Moti | Skia only if canvas needed |
| Bottom sheet | @gorhom/bottom-sheet | Settled winner |

## Aesthetic per app type

| App type | Vibe | Conductor stage 2 |
|----------|------|---------------------|
| Wellness / spiritual | Warm editorial | soft-skill OR design-references → Notion/Claude brand |
| AMOLED minimalist (sleep/meditation) | Pure black + 1 accent | brutalist-skill OR design-references → Linear/Tesla |
| Trading / data dashboard | Data-dense, mono numbers | taste-skill DENSITY=8 |
| Marketplace | Photographic hero | design-references → Airbnb |

## Verification (taskmaster, if installed)

The Stop hook blocks turn-end without proof of:
- App actually builds (`eas build --platform <p> --profile development`)
- App actually runs in simulator/device
- Type-check passes
- No `console.log` leaked to production

## Cost

- Pure local code, $0 in API calls
- EAS builds (cloud) — Free tier covers personal use; $19/mo if you exceed
