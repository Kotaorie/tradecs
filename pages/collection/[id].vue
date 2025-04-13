<template>
  <div>
    <h2 class="text-xl font-semibold text-gray-900 sm:text-2xl ml-20 mt-20">{{ collection.name }}</h2>
		<div class="grid grid-cols-5 place-items-center gap-4 mx-20 mt-20">
			<SkinsSkin v-for="c in uniqueSkins().sort()" :key="c.id" :name="c.name" :id="c.id" :image="c.img_url" :color="c.color"/>
		</div>
  </div>
</template>

<script setup>
const route = useRoute();
const supabase = useSupabaseClient()
const id = route.params.id;
const {data: collection} = await supabase
	.from('collections')
	.select('name')
	.eq('id', id)
	.single()

let { data } = await supabase
	.from('skin')
	.select('name, id, img_url, rarityId')
	.eq('collectionId', route.params.id) 


let { data: rarity } = await supabase
  .from('rarity')
  .select('*')

const uniqueSkins = () => {
	const uniqueNames = new Set();
	const filteredSkins = data.filter(skin => {
		if (!uniqueNames.has(skin.name)) {
			uniqueNames.add(skin.name);
			return true;
		}
		return false;
	});
	return filteredSkins.map(skin => {
		skin.rarity = rarity.find(r => r.id === skin.rarityId)?.value || '';
		if (skin.rarity === 1) {
			skin.color = '#afafaf';
		} else if (skin.rarity === 2) {
			skin.color = '#6496e1';
		} else if (skin.rarity === 3) {
			skin.color = '#4b69cd';
		} else if (skin.rarity === 4) {
			skin.color = '#8847ff';
		} else if (skin.rarity === 5) {
			skin.color = '#d32ce6';
		} else if (skin.rarity === 6) {
			skin.color = '#eb4b4b';
		}
		return skin;	
	}).sort((a, b) => b.rarity - a.rarity); // Sort by rarity in descending order
};

</script>
