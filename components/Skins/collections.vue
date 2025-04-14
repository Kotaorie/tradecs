<template>
    <div @click="goToCollection(id)" class="flex flex-col items-center justify-center cursor-pointer bg-gray-200/50 p-4 rounded-lg shadow-md hover:bg-gray-300 transition duration-300 ease-in-out">
        <div class="w-full h-32 overflow-hidden rounded-lg mb-2">
            <img :src="image" :alt="name" class="h-32 object-cover object-center transition-transform duration-300 ease-in-out transform hover:scale-105" />
        </div>
        <p class="text-sm mb-4">{{ name }}</p>
    </div>
</template>

<script setup>
const router = useRouter()
defineProps({
  name: String,
  id: String,
	image: String,
})

const goToCollection = (id) => {
  router.push(`/collection/${id}`);
};
</script>