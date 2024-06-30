# week7

## 性能の考察

### First Fit

利点：実装が簡単で、実行は他より早い

欠点：小さな未使用ブロックが蓄積される


### Best Fit:

利点：utilizationがfirstfitより高かった。first fit より小さい未使用領域がなさそう

欠点：毎回リスト全体を見ているため、割り当て操作が遅い。

→　未使用領域の先頭に次の領域の未使用領域の空間をおいておく


### Worst Fit

利点: 大きな空き領域を維持しやすい

欠点: メモリの断片化が進みやすく、非効率になりやすい。また、Best Fitと同様に常にO(n)の時間がかかる。

### Free list bin 

利点：utilizationが高くなる。メモリの無駄がへる

欠点：データによっては使われないbinがあるため無駄になるかも。

best_fit
```
void *my_malloc(size_t size) {
  my_metadata_t *metadata = my_heap.free_head;
  my_metadata_t *prev = NULL;

  my_metadata_t *best_fit = NULL;
  my_metadata_t *best_fit_prev = NULL;
  size_t best_fit_size = SIZE_MAX;
   // 未使用領域の中で最もデータに合う小さい領域を探す
  while (metadata) {
    if (metadata->size >= size && metadata->size < best_fit_size) {
      best_fit = metadata;
      best_fit_prev = prev;
      best_fit_size = metadata->size;
    }
    prev = metadata;
    metadata = metadata->next;
  }
  // now, metadata points to the first free slot
  // and prev is the previous entry.

  if (!best_fit) {
    // There was no free slot available. We need to request a new memory region
    // from the system by calling mmap_from_system().
    //
    //     | metadata | free slot |
    //     ^
    //     metadata
    //     <---------------------->
    //            buffer_size
    size_t buffer_size = 4096;
    my_metadata_t *new_metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    if (!new_metadata) return NULL; // mmap failed
    new_metadata->size = buffer_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // Add the memory region to the free list.
    my_add_to_free_list(new_metadata);
    // Now, try my_malloc() again. This should succeed.
    return my_malloc(size);
  }

  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr



  // void *ptr = metadata + 1;
  // size_t remaining_size = metadata->size - size;
  size_t remaining_size = best_fit->size - size;
  // Remove the free slot from the free list.
  my_remove_from_free_list(best_fit, best_fit_prev);

  // Calculate remaining size after allocation
  if (remaining_size > sizeof(my_metadata_t)) {
    // Shrink the metadata for the allocated object
    // to separate the rest of the region corresponding to remaining_size.
    // If the remaining_size is not large enough to make a new metadata,
    // this code path will not be taken and the region will be managed
    // as a part of the allocated object.
     my_metadata_t *new_metadata = (my_metadata_t *)((char *)(best_fit + 1) + size);

    // Create a new metadata for the remaining free slot.
    //
    // ... | metadata | object | metadata | free slot | ...
    //     ^          ^        ^
    //     metadata   ptr      new_metadata
    //                 <------><---------------------->
    //                   size       remaining size
   
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // Add the remaining free slot to the free list.
    my_add_to_free_list(new_metadata);
    best_fit->size = size;
  }



  return best_fit + 1;
}
```

worst_list
```
void *my_malloc(size_t size) {
  my_metadata_t *metadata = my_heap.free_head;
  my_metadata_t *prev = NULL;

  my_metadata_t *worst_fit = NULL;
  my_metadata_t *worst_fit_prev = NULL;
  size_t worst_fit_size = 0; // 最悪適合のサイズを追跡するために0から開始

  // 最悪適合: 要求されたサイズより大きい中で最も大きなブロックを見つける
  while (metadata) {
    if (metadata->size >= size && metadata->size > worst_fit_size) {
      worst_fit = metadata;
      worst_fit_prev = prev;
      worst_fit_size = metadata->size;
    }
    prev = metadata;
    metadata = metadata->next;
  }

  if (!worst_fit) {
    // 利用可能な空きスロットがない場合、新しいメモリ領域をシステムから要求
    size_t buffer_size = 4096;
    my_metadata_t *new_metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    if (!new_metadata) return NULL; // mmap失敗
    new_metadata->size = buffer_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    my_add_to_free_list(new_metadata);
    return my_malloc(size); // 再試行
  }

  // 割り当て
  size_t remaining_size = worst_fit->size - size;
  my_remove_from_free_list(worst_fit, worst_fit_prev);

  if (remaining_size > sizeof(my_metadata_t)) {
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)(worst_fit + 1) + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    my_add_to_free_list(new_metadata);
    worst_fit->size = size;
  }

  return worst_fit + 1;
}
```