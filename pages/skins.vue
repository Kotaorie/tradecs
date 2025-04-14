<template>
  <div>
    <div class="mt-10">
      <SkinsSearch :weapon="skins" :collection="data" @collection="selectedCollection"/>
    </div>
    <div class="grid grid-cols-8 place-items-center gap-4 mx-20 mt-20">
      <SkinsCollections v-for="c in collections" :key="c.id" :name="c.name" :id="c.id" :image="c.img_url"/>
    </div>
  </div>
</template>

<script setup>
const supabase = useSupabaseClient()
let collections = ref([])

  let { data, error } = await supabase
  .from('collections')
  .select('*')

  if(data){
    collections.value = data
  }

  let { data: skins, error: skinsError } = await supabase
  .from('type')
  .select('*')

function selectedCollection(collection) {
  if (!collection) {
    collections.value = data
    return
  }else {
    collections.value = data.filter((item) => item.name === collection)
    console.log('Selected collection:', collection)
  }
}
</script>
