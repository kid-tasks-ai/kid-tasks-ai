declare module "@vue/runtime-core" {
    export interface GlobalComponents {
        UButton: typeof import('@nuxt/ui')['UButton']
        UCard: typeof import('@nuxt/ui')['UCard']
        UInput: typeof import('@nuxt/ui')['UInput']
        UFormGroup: typeof import('@nuxt/ui')['UFormGroup']
        UAlert: typeof import('@nuxt/ui')['UAlert']
        UTextarea: typeof import('@nuxt/ui')['UTextarea']
        USelect: typeof import('@nuxt/ui')['USelect']
        UProgress: typeof import('@nuxt/ui')['UProgress']
        UModal: typeof import('@nuxt/ui')['UModal']
    }
}

export {}