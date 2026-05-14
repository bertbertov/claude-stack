---
name: react-native-apps
description: Complete skill for building, debugging, and shipping React Native / Expo apps in 2025-2026. Use when the user is building a mobile app, starting a new Expo project, debugging Expo Go crashes, setting up EAS builds, submitting to Google Play / App Store, writing animation patterns, or asking about mobile architecture decisions. Distilled from production Expo SDK 54 apps, official docs, Reddit r/reactnative hot threads, GitHub issues on expo/expo and facebook/react-native, and teardowns of shipped apps (Elirox, Instamobile templates). Covers 13 gotchas, 13 UX patterns, full deployment pipeline, animation stack, and production architecture boilerplate.
version: 1.0.0
user-invocable: false
---

# React Native / Expo App Building — Complete Reference

Use this as the authoritative guide when building any React Native app. When context is small, just follow the key rules. When the user hits a specific problem, jump to the matching section.

---

## Specialist Expo skills (defer to these for specifics)

For deep-dive on a specific Expo concern, defer to the official Expo team skills installed alongside this one:

| Concern | Use this specialist |
|---|---|
| Upgrading SDK (54 → 55, dependency hell) | **upgrading-expo** |
| Building/distributing dev clients | **expo-dev-client** |
| Build & ship to App Store / Play Store / Web | **expo-deployment** |
| EAS Workflows YAML / CI-CD | **expo-cicd-workflows** |
| OTA update health (crash rate, install count) | **eas-update-insights** |
| Native module authoring (Swift/Kotlin/TS) | **expo-module** |
| API routes via Expo Router + EAS Hosting | **expo-api-routes** |
| Universal data fetching, caching, mutations | **native-data-fetching** |
| UI fundamentals + styling + components | **building-native-ui** |
| Tailwind v4 + NativeWind v5 setup | **expo-tailwind-setup** |
| `@expo/ui` Jetpack Compose interop | **expo-ui-jetpack-compose** |
| `@expo/ui` SwiftUI interop | **expo-ui-swift-ui** |
| DOM components (run web in webview) | **use-dom** |

Use this skill (`react-native-apps`) for stack defaults, architecture, and the 13 gotchas. Use the specialist skills above when the task is narrow and deep.

---

## 0. STACK DEFAULTS (2025-2026)

| Concern | Default pick | Why |
|---|---|---|
| Framework | **Expo SDK 54+** with `expo-router` | File-based routing, typed routes, auth gating, works on iOS/Android/Web |
| Navigation | `expo-router` route groups `(auth)`/`(tabs)`/`(onboarding)` | Declarative, collocated with screens |
| Language | **Strict TypeScript** (`"strict": true`, `noUncheckedIndexedAccess`) | Mandatory for teams, saves you from silent bugs |
| Client state | **Zustand** (~1KB, selector-based) | Tiny, fast, no provider, works outside React |
| Server state | **TanStack Query v5** | Caching, retries, optimistic updates |
| Storage | **react-native-mmkv** (sync, 30× faster than AsyncStorage) | Needs dev build. Fallback: AsyncStorage |
| Secrets | `expo-secure-store` | Keychain/Keystore — never AsyncStorage for tokens |
| API client | `fetch` + thin wrapper OR `axios` | Fetch wins for most cases |
| Validation | **Zod** at API boundaries | Runtime type-safety, infer static types |
| Auth | **Clerk** or **Supabase Auth** | Ship fast. Custom JWT only if required |
| Animation | **Reanimated 3/4 + Moti** (Skia only if canvas needed) | See Section 4 |
| Bottom sheet | `@gorhom/bottom-sheet` | Settled winner. Built on Reanimated + gesture-handler |
| Charts | `react-native-wagmi-charts` (simple) / `victory-native` v40 Skia (complex) | Native perf |
| Icons | `@phosphor-icons/react-native` or `@expo/vector-icons` | Tree-shakeable |
| Forms | `react-hook-form` + `zod` + `react-native-mask-input` | Standard combo |
| Errors | **Sentry** via `@sentry/react-native/expo` | Uploads sourcemaps on EAS build |
| E2E tests | **Maestro** (YAML) | Far less pain than Detox |
| Unit tests | Jest + React Native Testing Library + MSW | User-centric, mock network at fetch |
| Build | **EAS Build** (30 free builds/mo) | No local Xcode/JDK needed |
| CI | GitHub Actions + `expo/expo-github-action` | Auto-deploy on push |
| OTA | **EAS Update** (1000 free MAU) | Push JS fixes without rebuilding |

---

## 1. PROJECT ARCHITECTURE

### Folder Structure (Expo Router + Feature-Oriented)

```
my-app/
├── app/                          # expo-router (file-based routing)
│   ├── _layout.tsx               # Root providers (QueryClient, ErrorBoundary, ThemeProvider)
│   ├── index.tsx                 # Landing / redirect based on auth
│   ├── (onboarding)/             # Route group — onboarding flow
│   │   ├── _layout.tsx
│   │   ├── welcome.tsx
│   │   └── disclaimer.tsx
│   ├── (auth)/                   # Route group — auth stack
│   │   ├── _layout.tsx
│   │   ├── sign-in.tsx
│   │   └── sign-up.tsx
│   ├── (tabs)/                   # Route group — main tab nav
│   │   ├── _layout.tsx
│   │   ├── home.tsx
│   │   ├── bots.tsx
│   │   └── profile.tsx
│   └── +not-found.tsx
├── src/
│   ├── components/
│   │   ├── ui/                   # Button, Input, Card (design system)
│   │   └── features/             # Feature-specific composites
│   ├── hooks/                    # useAuth, useTheme, useDebounce
│   ├── services/
│   │   ├── api/
│   │   │   ├── client.ts         # fetch wrapper
│   │   │   └── endpoints/
│   │   └── queries/              # TanStack Query hooks
│   ├── store/                    # Zustand stores
│   ├── lib/                      # mmkv, constants, formatters
│   ├── types/
│   └── utils/
├── assets/
├── app.config.ts                 # typed over app.json
├── eas.json
└── tsconfig.json                 # strict: true, paths: {"@/*": ["src/*"]}
```

Keep `app/` thin — it's routing only. Real logic lives in `src/`.

### Canonical Boilerplate

**`src/lib/storage.ts`** — MMKV wrapper usable with Zustand's persist:
```ts
import { MMKV } from 'react-native-mmkv';
export const storage = new MMKV({ id: 'app', encryptionKey: 'rotate-me' });
export const mmkvZustandStorage = {
  getItem: (k: string) => storage.getString(k) ?? null,
  setItem: (k: string, v: string) => storage.set(k, v),
  removeItem: (k: string) => storage.delete(k),
};
```

**`src/store/auth.store.ts`** — Zustand + persist:
```ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { mmkvZustandStorage } from '@/lib/storage';

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null, token: null,
      signIn: (user, token) => set({ user, token }),
      signOut: () => set({ user: null, token: null }),
    }),
    { name: 'auth', storage: createJSONStorage(() => mmkvZustandStorage) }
  )
);
```

**`src/services/api/client.ts`** — fetch wrapper with auto-logout on 401:
```ts
import Constants from 'expo-constants';
import { useAuthStore } from '@/store/auth.store';
const BASE = Constants.expoConfig?.extra?.API_URL as string;

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = useAuthStore.getState().token;
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...init.headers,
    },
  });
  if (res.status === 401) useAuthStore.getState().signOut();
  if (!res.ok) throw new ApiError(res.status, await res.text());
  return res.json();
}
```

**`app/_layout.tsx`** — providers at root:
```tsx
import { Stack } from 'expo-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { BottomSheetModalProvider } from '@gorhom/bottom-sheet';
import { ErrorBoundary } from 'react-error-boundary';

const qc = new QueryClient({ defaultOptions: { queries: { retry: 2 } } });

export default function RootLayout() {
  return (
    <ErrorBoundary fallback={<CrashScreen />}>
      <GestureHandlerRootView style={{ flex: 1 }}>
        <SafeAreaProvider>
          <QueryClientProvider client={qc}>
            <BottomSheetModalProvider>
              <Stack screenOptions={{ headerShown: false }} />
            </BottomSheetModalProvider>
          </QueryClientProvider>
        </SafeAreaProvider>
      </GestureHandlerRootView>
    </ErrorBoundary>
  );
}
```

**Environment variables**: `app.config.ts` with `extra` + `expo-constants`. Secrets go into **EAS Secrets** (`eas secret:create`), never in committed `.env`. Public client values use `EXPO_PUBLIC_*` prefix (auto-inlined at build).

---

## 2. UX PATTERNS (Premium Mobile 2025-2026)

### 2.1 Onboarding — "Pre-onboarding first, auth last"
Show value BEFORE asking for email. Reduces drop-off 20-40%. Sequence:
Splash (1.5s) → 3-4 value slides (`react-native-pager-view` + Reanimated) → risk disclaimer (if regulated) → optional signup → personalization quiz → main app.

Persist completion in MMKV. Auth-gate via expo-router groups:
```tsx
<Stack>
  {!hasOnboarded ? <Stack.Screen name="(onboarding)" /> :
   !isAuthed ? <Stack.Screen name="(auth)" /> :
   <Stack.Screen name="(tabs)" />}
</Stack>
```

### 2.2 Bottom Tab Nav — Floating Pill
Telegram/Revolut style. Sits 16-24px above safe-area, rounded-full, dark blur bg, 5 icons max.
```tsx
<Tabs screenOptions={{
  tabBarStyle: {
    position: 'absolute', bottom: insets.bottom + 16, marginHorizontal: 24,
    borderRadius: 999, height: 64, backgroundColor: 'rgba(20,20,20,0.85)',
    borderTopWidth: 0, elevation: 12,
  }
}} />
```
Morphing variant (Spotify-style): center tab is FAB that opens a gorhom bottom sheet.

### 2.3 Empty States
Rule: illustration + one-line empathy + single CTA. NEVER "No data."
- No bots: *"Your trading floor is quiet. Launch your first strategy to wake it up."* [Browse →]
- No trades: *"Once Diana spots a sweep, trades show here."* [See how →]

Use `react-native-svg` for crisp illustrations. Centered column, 40% vertical padding.

### 2.4 Card Patterns
- **Expandable in place:** `Animated.View` with `layout={LinearTransition.springify()}`
- **Swipeable:** `react-native-gesture-handler` `Swipeable`
- **Stacked (Tinder):** `react-native-deck-swiper` or custom `PanGestureHandler`

### 2.5 Modal / Bottom Sheet
**`@gorhom/bottom-sheet` is the settled winner.**
```tsx
<BottomSheetModal ref={ref} snapPoints={['25%','60%','90%']}
  enableDynamicSizing={false}
  backdropComponent={BottomSheetBackdrop}>
  <BottomSheetView>{/* content */}</BottomSheetView>
</BottomSheetModal>
```

### 2.6 Skeleton vs Spinner
- Known shape → skeleton with shimmer (Reanimated gradient sweep, 1.2s loop)
- Unknown duration / foreground action → spinner button (disabled, `ActivityIndicator` inside)

### 2.7 Haptics (map intent → type)
```ts
Haptics.selectionAsync()                                       // tap nav/button
Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)        // confirm action
Haptics.notificationAsync(Haptics.NotificationFeedbackStyle.Success)
Haptics.notificationAsync(Haptics.NotificationFeedbackStyle.Error)
```
Wrap every `Pressable` that triggers state change.

### 2.8 Forms — RHF + Zod
Floating labels. Validate **on blur**, not on-change (jarring). Submit button disabled until `formState.isValid`. Errors slide-in via Reanimated `FadeInDown`.

### 2.9 Charts — two-tier
- **Micro-chart / spark:** `react-native-wagmi-charts <LineChart>` (simple, haptic cursor)
- **Candlesticks / indicators:** `victory-native` v40+ (Skia-backed) or `lightweight-charts` via WebView

### 2.10 Theme Switching — smooth
`useColorScheme` + Reanimated shared value, 300ms fade. Interpolate via `interpolateColor`. Don't remount — causes jank.
```tsx
const progress = useSharedValue(isDark ? 1 : 0);
useEffect(() => { progress.value = withTiming(isDark ? 1 : 0, {duration:300}); }, [isDark]);
const bg = useAnimatedStyle(() => ({
  backgroundColor: interpolateColor(progress.value,[0,1],['#fff','#0a0a0a'])
}));
```
Or drop in `react-native-theme-switch-animation` for circular reveal.

### 2.11 Onboarding Checklist
Drives day-1 retention. Pin a collapsible "Get started" card on home until tasks complete. Each row: circle → checkmark (Reanimated spring), row crosses out. Auto-dismiss at 3/4 done.

### 2.12 Pull-to-Refresh (custom)
Default `RefreshControl` feels cheap. Custom:
```tsx
const scrollY = useSharedValue(0);
const onScroll = useAnimatedScrollHandler(e => { scrollY.value = e.contentOffset.y; });
const style = useAnimatedStyle(() => ({
  transform: [{ rotate: `${interpolate(scrollY.value,[0,-80],[0,360])}deg` }],
  opacity: interpolate(scrollY.value,[0,-40],[0,1]),
}));
```

### 2.13 Elirox Pattern (trading-app reference)
- **Demo must be default path.** Don't require broker before value.
- **"AI Preset" framing converts better** than "Pick a strategy."
- **Create-bot as 4-step wizard** in bottom sheet pages, not a single long form: asset → strategy → risk → launch.
- **Paywall triggers on action** ("Launch Live"), not on app open.
- **Bottom tabs:** 4 tabs (Home · Bots · Analytics · Profile) + center "+" as create shortcut.

---

## 3. ANIMATION STACK

### Library hierarchy (use in this order)

| Library | When |
|---|---|
| **Reanimated 3/4** (default) | Anything gesture-driven, 60/120fps, worklets on UI thread. Works in Expo Go. |
| **Moti** | Declarative wrapper over Reanimated. Great for staggered lists, onboarding, marketing UI. |
| **Skia** (`@shopify/react-native-skia`) | Custom canvas — particles, shaders, liquid swipe, premium shimmer. **Requires dev build.** |
| **Lottie** | Pre-made After Effects animations (success checkmarks, mascots). Works in Expo Go. |
| **Animated API** | Legacy only. Keep for existing code. |

### Canonical patterns

**Press feedback (scale 0.97):**
```tsx
const scale = useSharedValue(1);
const style = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }] }));
// onPressIn: scale.value = withSpring(0.97, { damping: 15, stiffness: 300 });
// onPressOut: scale.value = withSpring(1);
```

**Staggered list fade-in (Moti):**
```tsx
<MotiView from={{ opacity: 0, translateY: 20 }} animate={{ opacity: 1, translateY: 0 }}
  transition={{ type: 'spring', delay: index * 60 }} />
```

**Pulse / breathing:**
```tsx
scale.value = withRepeat(withSequence(
  withTiming(1.05, { duration: 800 }),
  withTiming(1, { duration: 800 })
), -1, true);
```

**Number count-up (TextInput trick):**
```tsx
const value = useSharedValue(0);
useEffect(() => { value.value = withTiming(527.45, { duration: 1200 }); }, []);
const animatedProps = useAnimatedProps(() => ({ text: `$${value.value.toFixed(2)}` }));
// Render with Animated.createAnimatedComponent(TextInput), editable={false}
```

**Parallax scroll:**
```tsx
const scrollY = useSharedValue(0);
const onScroll = useAnimatedScrollHandler(e => { scrollY.value = e.contentOffset.y; });
const headerStyle = useAnimatedStyle(() => ({
  transform: [{ translateY: scrollY.value * 0.5 }],
  opacity: interpolate(scrollY.value, [0, 200], [1, 0]),
}));
```

### Performance rules

1. Reanimated worklets > Animated API for gesture-driven or >2 simultaneous animations
2. Old Animated API: always `useNativeDriver: true` + only animate `opacity`/`transform`. Never `width`/`height`/`backgroundColor` on native driver — silently fails
3. Layout animations: Reanimated's `Layout` prop OR animate `scale + translate` instead of real layout for 120Hz
4. Worklets must be pure — no closures over React state. Pass via shared values
5. `runOnJS(cb)()` (renamed to `scheduleOnRN` in Reanimated 4) costs a frame — use sparingly
6. FlatList rows: use Moti per-item, not `Animated.Value` mapping — memory cheaper

### Expo Go compatibility
| Library | Expo Go | Dev Build |
|---|---|---|
| Animated API | ✓ | ✓ |
| Reanimated | ✓ | ✓ |
| Moti | ✓ | ✓ |
| Lottie | ✓ | ✓ |
| **Skia** | **✗** | ✓ |
| `@gorhom/bottom-sheet` | ✓ | ✓ |
| `react-native-gesture-handler` | ✓ | ✓ |

---

## 4. PRODUCTION GOTCHAS (13 things to check first)

### 4.1 Expo Go SDK version mismatch
Expo Go ships ONE SDK at a time. Your project SDK must match. Error: *"Project is incompatible with this version of Expo Go."*
**Fix:** update Expo Go from store, or use `expo-dev-client` so your build pins its own SDK.

### 4.2 `newArchEnabled` / `edgeToEdgeEnabled`
- SDK 54 is the **last** version where New Arch can be disabled. SDK 55+ (RN 0.82) has it forced on.
- Android 15 (targetSdk 35) forces edge-to-edge regardless of `edgeToEdgeEnabled=false` — status/nav bars go transparent.
- **Tabs component from expo-router crashes in Expo Go SDK 54.** Workaround: build a custom bottom nav or use dev-client.
- **Right:** install `react-native-edge-to-edge` + `react-native-safe-area-context`, read insets via `useSafeAreaInsets()`, render with `SystemBars` component.

### 4.3 BackHandler (Android)
`addEventListener` returns a subscription now.
```tsx
// RIGHT — focus-scoped, cleaned up
useFocusEffect(useCallback(() => {
  const sub = BackHandler.addEventListener('hardwareBackPress', () => true);
  return () => sub.remove();
}, []));
```

### 4.4 AsyncStorage vs localStorage
Sync (`localStorage`) vs async (`AsyncStorage`) — NOT interchangeable. 6MB cap, plaintext. Use `expo-secure-store` for tokens. On web, `@react-native-async-storage/async-storage` polyfills over localStorage as async.

### 4.5 Font loading race
`useFonts` can return `[true, null]` before fonts finish, producing invisible text or infinite splash.
```tsx
SplashScreen.preventAutoHideAsync();
const [loaded, error] = useFonts({ Inter: require('./Inter.ttf') });
useEffect(() => { if (loaded || error) SplashScreen.hideAsync(); }, [loaded, error]);
if (!loaded && !error) return null;
```
Always log `error`. On Android, pre-bundle via `expo-font` config plugin instead of runtime.

### 4.6 SafeAreaProvider required
`useSafeAreaInsets()` silently returns zeros without a provider. Built-in `SafeAreaView` from `react-native` is **deprecated** — use community one.
```tsx
<SafeAreaProvider><RootNavigator/></SafeAreaProvider>
// screens:
const insets = useSafeAreaInsets();
<View style={{ paddingTop: insets.top }}/>
```

### 4.7 Pressable vs TouchableOpacity
`TouchableOpacity` wraps children in an extra `Animated.View`, breaking flex layouts inside `flex:1` parents. **Prefer `Pressable` in new code.**
```tsx
<Pressable style={({ pressed }) => [styles.btn, pressed && { opacity: 0.6 }]} hitSlop={8} />
```

### 4.8 Reanimated 4 migration
- Requires New Architecture only (no Paper)
- Worklets moved to `react-native-worklets`
- `babel.config.js`: `'react-native-reanimated/plugin'` → `'react-native-worklets/plugin'`
- `runOnJS`/`runOnUI` → `scheduleOnRN`/`scheduleOnUI`
- Removed: `useWorkletCallback`, `combineTransition`, `addWhitelistedNativeProps`
- Still on Paper? Stay on 3.x

### 4.9 Metro cache — when to `--clear`
Required after editing: `babel.config.js`, `metro.config.js`, `tsconfig.json` paths, SVG transformer, installing/removing native modules.
Nuclear: `watchman watch-del-all && rm -rf node_modules $TMPDIR/metro-* && npx expo start --clear`

### 4.10 Hot reload stale — `r` vs rescan
- `r` suffices for JS changes
- MUST rescan QR / rebuild when: changing `app.json`, adding native module, editing `metro.config.js`, after `expo prebuild`
- **Expo Go caches old project URL** — scan fresh QR each server restart, don't tap history

### 4.11 KeyboardAvoidingView
Android 15 + targetSdk 35 breaks it. Use `react-native-keyboard-controller`'s `KeyboardAvoidingView` in 2025+.
```tsx
<KeyboardAvoidingView
  behavior={Platform.OS === 'ios' ? 'padding' : undefined}
  keyboardVerticalOffset={headerHeight}
  style={{ flex: 1 }} />
```
Set `android:windowSoftInputMode="adjustResize"` in AndroidManifest.

### 4.12 FlatList inside ScrollView
Nesting same-orientation VirtualizedList in ScrollView kills virtualization and breaks touch on Android.
```tsx
// WRONG: <ScrollView><FlatList /></ScrollView>
// RIGHT:
<FlatList
  data={items}
  ListHeaderComponent={<HeroSection/>}
  ListFooterComponent={<Footer/>}
  removeClippedSubviews
  keyExtractor={(i) => i.id}
  renderItem={renderItem} // memoized outside component
/>
```

### 4.13 Perf micro-gotchas
- Inline style arrays `style={[s.box, {mt:10}]}` create new refs every render — hoist
- Memoize `renderItem` and `keyExtractor`
- `useCallback` for list row `onPress`
- Expo Updates on iOS: keep `:hermes_enabled` in Podfile or OTA bundles fail

---

## 5. DEPLOYMENT — EAS Build + Google Play

### 5.1 eas.json (three standard profiles)

```json
{
  "cli": { "version": ">= 12.0.0", "appVersionSource": "remote" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "android": { "buildType": "apk" }
    },
    "preview": {
      "distribution": "internal",
      "channel": "preview",
      "android": { "buildType": "apk" }
    },
    "production": {
      "channel": "production",
      "autoIncrement": true,
      "android": { "buildType": "app-bundle" }
    }
  },
  "submit": {
    "production": {
      "android": { "serviceAccountKeyPath": "./google-service-account.json", "track": "internal" }
    }
  }
}
```

### 5.2 Build commands
```bash
npm install -g eas-cli
eas login
eas build:configure
eas build --platform android --profile preview      # APK for sideload
eas build --platform android --profile production   # AAB for Play
eas build --local                                    # free, skip queue
```

**Free tier (2026):** 15 Android + 15 iOS builds/month. Queue 10min–2hr on free. Production plan $199/mo for priority queue.

### 5.3 app.json required fields
```json
{
  "expo": {
    "name": "Your App",
    "slug": "your-app",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "scheme": "yourapp",
    "userInterfaceStyle": "automatic",
    "splash": { "image": "./assets/splash.png", "resizeMode": "contain", "backgroundColor": "#000" },
    "android": {
      "package": "com.yourorg.yourapp",
      "versionCode": 1,
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#FFD700",
        "monochromeImage": "./assets/monochrome-icon.png"
      }
    },
    "ios": { "bundleIdentifier": "com.yourorg.yourapp", "buildNumber": "1" },
    "updates": { "url": "https://u.expo.dev/<project-id>" },
    "runtimeVersion": { "policy": "appVersion" },
    "plugins": [
      ["expo-build-properties", { "android": { "compileSdkVersion": 35, "targetSdkVersion": 35 } }],
      "expo-updates"
    ],
    "extra": { "eas": { "projectId": "..." } }
  }
}
```

**Gotcha:** Package name and bundleIdentifier are immutable once published.

### 5.4 Icons
- Master: 1024×1024 PNG, square, fully opaque, no rounded corners (OS masks)
- Adaptive (Android): foreground (center 66×66 dp safe), background color, monochrome (Android 13+ themed)
- Splash: 1200×1200 transparent PNG, `imageWidth` max 200

### 5.5 Android signing
EAS auto-manages keystore. On first build it generates one — say yes.
```bash
eas credentials    # interactive management
eas credentials -p android --profile production    # export
```
Save keystore + password + alias + key password to password manager. **Losing them bricks your Play listing forever.**

### 5.6 Google Play submission
- **$25 one-time** registration
- **Personal vs Organization** account — permanent choice. Organization skips 12-tester rule.
- **Target API 35** (Android 15) required after Aug 31 2025 for new apps and updates
- **Data Safety form** (mandatory, 2025+): declare every SDK (Sentry, Firebase, Stripe, analytics). Lying = permanent ban
- **Release tracks:**
  1. Internal testing (100 testers, instant)
  2. Closed testing (12 opted-in testers × **14 days** for personal accounts — strict clock)
  3. Open testing (optional)
  4. Production (requires prior closed test pass)
- **Store listing:** short desc 80ch, long desc 4000ch, app icon 512×512, feature graphic 1024×500, 2-8 phone screenshots, privacy policy URL (HTTPS, no PDF)
- **AAB only** — APK uploads to production no longer allowed

### 5.7 OTA via EAS Update
JS-only changes without rebuild:
```bash
npx expo install expo-updates
eas update:configure
eas update --branch production --message "Fix button color"
eas channel:edit production --branch production
```
Runtime version must match binary's. Use `"runtimeVersion": {"policy": "appVersion"}`. Native module changes still need a new binary.

### 5.8 Sentry (crash reporting)
```bash
npx expo install @sentry/react-native
```
`app.json`:
```json
["@sentry/react-native/expo", { "organization": "your-org", "project": "your-app" }]
```
`App.tsx`:
```ts
import * as Sentry from '@sentry/react-native';
Sentry.init({ dsn: 'https://xxx@sentry.io/xxx', tracesSampleRate: 0.2, enableNative: true });
export default Sentry.wrap(App);
```
Store `SENTRY_AUTH_TOKEN` as EAS secret. Sourcemaps upload automatically.

### 5.9 Privacy policy generators (free, Play-accepted)
- **Termly** — GDPR/CCPA ready
- **FreePrivacyPolicy.com** — mobile template
- **nisrulz/app-privacy-policy-generator** (open source, host on GitHub Pages)
Must be HTTPS URL, no PDF, no popup.

### 5.10 Trading / financial app framing
To avoid policy rejection without broker licensing:
- Frame as **"educational / simulation / signal information"** not "trading" or "investment advice"
- Short desc: *"Educational trading signals and market insights for learners"* — never *"Make money trading"*
- Risk disclaimer prominent on first launch AND in settings: *"This app does not provide financial advice. Trading involves risk of loss."*
- Don't execute real trades inside app without broker license in target country — link externally
- Content rating: "References to gambling" = No (avoid 18+ bucket)
- **Premium tiers: use Google Play Billing** (required for digital content). External payment (Stripe) only for physical services
- Elirox-type survives by: educational framing, visible disclaimers, no unlicensed brokerage, Play Billing for subs, accurate Data Safety

### 5.11 Common rejections

| Reason | Fix |
|---|---|
| Privacy policy missing/broken | HTTPS URL, in-app AND store listing, lists every data type |
| Metadata misleading | Match description to functionality, no keyword stuffing |
| Permissions abuse | Remove unused with `blockedPermissions`, justify each |
| Crashes during review | Test release build on real low-end Android (API 30, 2GB RAM) |
| Target API too low | Bump to 35 via `expo-build-properties` |
| Data Safety mismatch | Declare every SDK exactly |
| Financial misrepresentation | Add risk disclaimer, frame educational, contact email |
| Closed testing bypass attempt | Run 12 testers × 14 days — no shortcut on personal accounts |
| Icon violations | 1024×1024 square, no alpha, no rounded corners |

### 5.12 GitHub Actions CI/CD
`.github/workflows/eas-build.yml`:
```yaml
name: EAS Build
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - uses: expo/expo-github-action@v8
        with: { eas-version: latest, token: ${{ secrets.EXPO_TOKEN }} }
      - run: npm ci
      - run: eas build --platform android --profile production --non-interactive --no-wait
      - run: eas update --branch production --message "${{ github.event.head_commit.message }}"
```

---

## 6. KEY RULES (the "remember these 10" list)

1. **Match Expo Go SDK to project SDK.** Or use dev-client.
2. **Wrap root in `SafeAreaProvider`** always. Hooks fail silently without it.
3. **Use `useFocusEffect` + subscription `.remove()`** for BackHandler, not raw useEffect.
4. **Scan fresh QR every server restart** — Expo Go caches the old URL.
5. **Reanimated > Animated API** for new code. Worklets on UI thread beat JS thread every time.
6. **MMKV > AsyncStorage** when you can use dev build. `expo-secure-store` for all secrets/tokens.
7. **Zustand > Context** for anything that changes. Context re-renders every consumer.
8. **Package/bundle ID is forever.** Don't rush this decision.
9. **Data Safety form: tell the truth.** Lying = permanent Play ban.
10. **Premium subs on mobile = Google Play Billing** (not Stripe) if content is digital. Physical services can use external payment.

---

## Sources
- Expo docs (docs.expo.dev), Expo blog, Expo changelogs SDK 50-55
- GitHub issues: expo/expo, facebook/react-native, software-mansion/react-native-reanimated
- Reddit r/reactnative hot threads 2024-2026
- Fernando Rojo (Moti creator) / Catalin Miron / William Candillon writings
- Gorhom bottom sheet, MMKV, gesture-handler, safe-area-context docs
- Google Play Console policy docs (Data Safety, API 35, testing tracks)
- Elirox app teardown (decompiled APK + App Store listing)
- Real-world ship-it threads: "mistakes I made", "how I shipped my first app"

Last updated: 2026-04.
