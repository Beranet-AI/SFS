"use client";

import { useI18nContext } from "@/i18n/I18nProvider";

export function useTranslation() {
  return useI18nContext();
}
