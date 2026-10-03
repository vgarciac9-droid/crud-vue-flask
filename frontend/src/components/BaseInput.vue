<template>
  <label class="field">
    <span>{{ label }}</span>
    <input
      :value="modelValue"
      :type="type"
      :placeholder="placeholder"
      :step="step"
      :min="min"
      @input="$emit('update:modelValue', $event.target.value)"
    />
    <small v-if="error" class="field__error">{{ error }}</small>
  </label>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  modelValue: { type: [String, Number], default: '' },
  type: { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  error: { type: String, default: '' },
  step: { type: String, default: undefined },
  min: { type: String, default: undefined },
})
defineEmits(['update:modelValue'])
</script>
