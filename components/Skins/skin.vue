<template>
	<div :style="{ backgroundColor: color }" class="flex flex-col items-center justify-center p-4 rounded-lg shadow-md hover:bg-gray-300 transition duration-300 ease-in-out">
		<div class="w-full h-64 overflow-hidden rounded-lg mb-2">
			<img :src="image" alt="">
		</div>
		<p class="text-sm mb-4">{{ name }}</p>
		<p class="text-sm mb-4">{{ price }}</p>
	</div>
</template>
<script setup>
defineProps({
  name: String,
  id: String,
	image: String,
	color: String,
	price: Number
})
</script>