/** @format */

import { useRouter } from "vue-router";

export default function useNavigation() {
  const router = useRouter();

  const navigateTo = (path) => {
    router.push(path);
  };

  return {
    navigateTo,
  };
}
