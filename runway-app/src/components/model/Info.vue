<script setup lang="ts">
// Info subcomponent of model detail
// Currently a "kitchen-sink" approach - needs a lot of cleanup!
import type { PropType } from 'vue'
import type { Model } from '@/models/Model'
import { MDBTable } from 'mdb-vue-ui-kit'

const props = defineProps({
    model: Object as PropType<Model>
})

const evtSource = new EventSource("http://localhost:5000/events?channel=model_fit", { withCredentials: true } )

evtSource.addEventListener("complete", (event) => {
    const event_json = JSON.parse(event.data)
    if (props.model && event_json['model_id'] == props.model.id) {
      props.model.fit_at = event_json['fit_at']
      props.model.fit_time_ms = event_json['fit_time_ms']
      props.model.train_score = event_json['train_score']
      props.model.val_score = event_json['val_score']
      props.model.other_scores = event_json['other_scores']
      props.model.other_attribs = event_json['other_attribs']
    }
})

</script>

<template>
    <MDBTable style="max-width: 800px">
        <tr>
            <th scope="row" class="w-25"><strong>Name</strong></th>
            <td>{{ model?.name }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Dataset</strong></th>
            <td class="d-flex"><RouterLink :to="'/datasets/' + model?.dataset_id" class="p-0">{{ model?.dataset_name }}</RouterLink></td>
        </tr>
        <tr>
            <th scope="row"><strong>Type</strong></th>
            <td>{{ model?.class_name }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Author</strong></th>
            <td>{{ model?.created_by }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Created</strong></th>
            <td>{{ model ? new Date(model.created_at).toLocaleString() : '' }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Updated</strong></th>
            <td>{{ model ? new Date(model.updated_at).toLocaleString() : '' }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Sharing</strong></th>
            <td>{{ model?.is_public ? "Public" : "Private" }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Target</strong></th>
            <td>{{ model?.target_name }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Features</strong></th>
            <td>{{ model?.feature_names}}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Parameters</strong></th>
            <td>{{ model?.params }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Fit at</strong></th>
            <td>{{ model?.fit_at && model.fit_at.toString() != 'None' ? new Date(model.fit_at).toLocaleString() : 'Not trained' }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Fit time (ms)</strong></th>
            <td>{{ model?.fit_time_ms && model.fit_at.toString() != 'None' ? model.fit_time_ms : 'Not trained' }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Train score</strong></th>
            <td>{{ model?.train_score == 0 ? 'Not trained' : model?.train_score }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Val score</strong></th>
            <td>{{ model?.val_score == 0 ? 'Not trained' : model?.val_score }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Other scores</strong></th>
            <td>{{ model?.val_score == 0 ? 'Not trained' : model?.other_scores }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Other Attributes</strong></th>
            <td>{{ model?.val_score == 0 ? 'Not trained' : model?.other_attribs }}</td>
        </tr>
    </MDBTable>
</template>