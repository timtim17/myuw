import {fetchBuilder, extractData, buildWith} from './model_builder';

const customActions = {
    fetch: fetchBuilder('/api/v1/library/', extractData, 'json'),
};

export default buildWith(
    {customActions},
);
