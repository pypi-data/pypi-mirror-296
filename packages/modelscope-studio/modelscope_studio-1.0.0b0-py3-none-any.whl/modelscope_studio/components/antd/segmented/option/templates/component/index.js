function R(e) {
  const {
    gradio: t,
    _internal: i,
    ...n
  } = e;
  return Object.keys(i).reduce((s, o) => {
    const r = o.match(/bind_(.+)_event/);
    if (r) {
      const u = r[1], l = u.split("_"), f = (...m) => {
        const d = m.map((a) => m && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
          type: a.type,
          detail: a.detail,
          timestamp: a.timeStamp,
          clientX: a.clientX,
          clientY: a.clientY,
          targetId: a.target.id,
          targetClassName: a.target.className,
          altKey: a.altKey,
          ctrlKey: a.ctrlKey,
          shiftKey: a.shiftKey,
          metaKey: a.metaKey
        } : a);
        return t.dispatch(u.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: d,
          component: n
        });
      };
      if (l.length > 1) {
        let m = {
          ...n.props[l[0]] || {}
        };
        s[l[0]] = m;
        for (let a = 1; a < l.length - 1; a++) {
          const h = {
            ...n.props[l[a]] || {}
          };
          m[l[a]] = h, m = h;
        }
        const d = l[l.length - 1];
        return m[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = f, s;
      }
      const _ = l[0];
      s[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return s;
  }, {});
}
function w() {
}
function U(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function X(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return w;
  }
  const i = e.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function g(e) {
  let t;
  return X(e, (i) => t = i)(), t;
}
const p = [];
function b(e, t = w) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function s(u) {
    if (U(e, u) && (e = u, i)) {
      const l = !p.length;
      for (const f of n)
        f[1](), p.push(f, e);
      if (l) {
        for (let f = 0; f < p.length; f += 2)
          p[f][0](p[f + 1]);
        p.length = 0;
      }
    }
  }
  function o(u) {
    s(u(e));
  }
  function r(u, l = w) {
    const f = [u, l];
    return n.add(f), n.size === 1 && (i = t(s, o) || w), u(e), () => {
      n.delete(f), n.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: s,
    update: o,
    subscribe: r
  };
}
const {
  getContext: q,
  setContext: j
} = window.__gradio__svelte__internal, Y = "$$ms-gr-antd-slots-key";
function D() {
  const e = b({});
  return j(Y, e);
}
const L = "$$ms-gr-antd-context-key";
function Z(e) {
  var u;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = F(), i = H({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((l) => {
    i.slotKey.set(l);
  }), B();
  const n = q(L), s = ((u = g(n)) == null ? void 0 : u.as_item) || e.as_item, o = n ? s ? g(n)[s] : g(n) : {}, r = b({
    ...e,
    ...o
  });
  return n ? (n.subscribe((l) => {
    const {
      as_item: f
    } = g(r);
    f && (l = l[f]), r.update((_) => ({
      ..._,
      ...l
    }));
  }), [r, (l) => {
    const f = l.as_item ? g(n)[l.as_item] : g(n);
    return r.set({
      ...l,
      ...f
    });
  }]) : [r, (l) => {
    r.set(l);
  }];
}
const A = "$$ms-gr-antd-slot-key";
function B() {
  j(A, b(void 0));
}
function F() {
  return q(A);
}
const G = "$$ms-gr-antd-component-slot-context-key";
function H({
  slot: e,
  index: t,
  subIndex: i
}) {
  return j(G, {
    slotKey: b(e),
    slotIndex: b(t),
    subSlotIndex: b(i)
  });
}
function J(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var M = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function i() {
      for (var o = "", r = 0; r < arguments.length; r++) {
        var u = arguments[r];
        u && (o = s(o, n(u)));
      }
      return o;
    }
    function n(o) {
      if (typeof o == "string" || typeof o == "number")
        return o;
      if (typeof o != "object")
        return "";
      if (Array.isArray(o))
        return i.apply(null, o);
      if (o.toString !== Object.prototype.toString && !o.toString.toString().includes("[native code]"))
        return o.toString();
      var r = "";
      for (var u in o)
        t.call(o, u) && o[u] && (r = s(r, u));
      return r;
    }
    function s(o, r) {
      return r ? o ? o + " " + r : o + r : o;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(M);
var Q = M.exports;
const T = /* @__PURE__ */ J(Q), {
  getContext: W,
  setContext: $
} = window.__gradio__svelte__internal;
function tt(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function i(s = ["default"]) {
    const o = s.reduce((r, u) => (r[u] = b([]), r), {});
    return $(t, {
      itemsMap: o,
      allowedSlots: s
    }), o;
  }
  function n() {
    const {
      itemsMap: s,
      allowedSlots: o
    } = W(t);
    return function(r, u, l) {
      s && (r ? s[r].update((f) => {
        const _ = [...f];
        return o.includes(r) ? _[u] = l : _[u] = void 0, _;
      }) : o.includes("default") && s.default.update((f) => {
        const _ = [...f];
        return _[u] = l, _;
      }));
    };
  }
  return {
    getItems: i,
    getSetItemFn: n
  };
}
const {
  getItems: bt,
  getSetItemFn: et
} = tt("segmented"), {
  SvelteComponent: nt,
  check_outros: st,
  component_subscribe: v,
  create_slot: it,
  detach: ot,
  empty: rt,
  flush: y,
  get_all_dirty_from_scope: lt,
  get_slot_changes: ct,
  group_outros: ut,
  init: ft,
  insert: at,
  safe_not_equal: _t,
  transition_in: I,
  transition_out: k,
  update_slot_base: mt
} = window.__gradio__svelte__internal;
function O(e) {
  let t;
  const i = (
    /*#slots*/
    e[18].default
  ), n = it(
    i,
    e,
    /*$$scope*/
    e[17],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(s, o) {
      n && n.m(s, o), t = !0;
    },
    p(s, o) {
      n && n.p && (!t || o & /*$$scope*/
      131072) && mt(
        n,
        i,
        s,
        /*$$scope*/
        s[17],
        t ? ct(
          i,
          /*$$scope*/
          s[17],
          o,
          null
        ) : lt(
          /*$$scope*/
          s[17]
        ),
        null
      );
    },
    i(s) {
      t || (I(n, s), t = !0);
    },
    o(s) {
      k(n, s), t = !1;
    },
    d(s) {
      n && n.d(s);
    }
  };
}
function dt(e) {
  let t, i, n = (
    /*$mergedProps*/
    e[0].visible && O(e)
  );
  return {
    c() {
      n && n.c(), t = rt();
    },
    m(s, o) {
      n && n.m(s, o), at(s, t, o), i = !0;
    },
    p(s, [o]) {
      /*$mergedProps*/
      s[0].visible ? n ? (n.p(s, o), o & /*$mergedProps*/
      1 && I(n, 1)) : (n = O(s), n.c(), I(n, 1), n.m(t.parentNode, t)) : n && (ut(), k(n, 1, 1, () => {
        n = null;
      }), st());
    },
    i(s) {
      i || (I(n), i = !0);
    },
    o(s) {
      k(n), i = !1;
    },
    d(s) {
      s && ot(t), n && n.d(s);
    }
  };
}
function yt(e, t, i) {
  let n, s, o, r, {
    $$slots: u = {},
    $$scope: l
  } = t, {
    gradio: f
  } = t, {
    props: _ = {}
  } = t;
  const m = b(_);
  v(e, m, (c) => i(16, r = c));
  let {
    _internal: d = {}
  } = t, {
    as_item: a
  } = t, {
    value: h
  } = t, {
    visible: x = !0
  } = t, {
    elem_id: C = ""
  } = t, {
    elem_classes: K = []
  } = t, {
    elem_style: S = {}
  } = t;
  const P = F();
  v(e, P, (c) => i(15, o = c));
  const [E, V] = Z({
    gradio: f,
    props: r,
    _internal: d,
    visible: x,
    elem_id: C,
    elem_classes: K,
    elem_style: S,
    as_item: a,
    value: h
  });
  v(e, E, (c) => i(0, s = c));
  const N = D();
  v(e, N, (c) => i(14, n = c));
  const z = et();
  return e.$$set = (c) => {
    "gradio" in c && i(5, f = c.gradio), "props" in c && i(6, _ = c.props), "_internal" in c && i(7, d = c._internal), "as_item" in c && i(8, a = c.as_item), "value" in c && i(9, h = c.value), "visible" in c && i(10, x = c.visible), "elem_id" in c && i(11, C = c.elem_id), "elem_classes" in c && i(12, K = c.elem_classes), "elem_style" in c && i(13, S = c.elem_style), "$$scope" in c && i(17, l = c.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    64 && m.update((c) => ({
      ...c,
      ..._
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    81824 && V({
      gradio: f,
      props: r,
      _internal: d,
      visible: x,
      elem_id: C,
      elem_classes: K,
      elem_style: S,
      as_item: a,
      value: h
    }), e.$$.dirty & /*$slotKey, $mergedProps, $slots*/
    49153 && z(o, s._internal.index || 0, {
      props: {
        style: s.elem_style,
        className: T(s.elem_classes, "ms-gr-antd-segmented-option"),
        id: s.elem_id,
        value: s.value,
        ...s.props,
        ...R(s)
      },
      slots: n
    });
  }, [s, m, P, E, N, f, _, d, a, h, x, C, K, S, n, o, r, l, u];
}
class ht extends nt {
  constructor(t) {
    super(), ft(this, t, yt, dt, _t, {
      gradio: 5,
      props: 6,
      _internal: 7,
      as_item: 8,
      value: 9,
      visible: 10,
      elem_id: 11,
      elem_classes: 12,
      elem_style: 13
    });
  }
  get gradio() {
    return this.$$.ctx[5];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), y();
  }
  get props() {
    return this.$$.ctx[6];
  }
  set props(t) {
    this.$$set({
      props: t
    }), y();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), y();
  }
  get as_item() {
    return this.$$.ctx[8];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), y();
  }
  get value() {
    return this.$$.ctx[9];
  }
  set value(t) {
    this.$$set({
      value: t
    }), y();
  }
  get visible() {
    return this.$$.ctx[10];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), y();
  }
  get elem_id() {
    return this.$$.ctx[11];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), y();
  }
  get elem_classes() {
    return this.$$.ctx[12];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), y();
  }
  get elem_style() {
    return this.$$.ctx[13];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), y();
  }
}
export {
  ht as default
};
